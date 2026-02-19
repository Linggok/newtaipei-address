# -*- coding: utf-8 -*-
"""
從桌面上板橋/板橋區資料夾的「新北市門牌位置數值資料」CSV 篩選中和區，輸出為 zhonghe_real_data.csv
"""
import pandas as pd
import os

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

# 可能的來源路徑（板橋、板橋區資料夾，或桌面上的完整門牌資料）
source_paths = [
    os.path.join(desktop, '板橋', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '板橋區', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
]

base_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(base_dir, 'zhonghe_real_data.csv')

# 中和區 areacode（新北市門牌位置數值資料常用格式）
ZHONGHE_AREACODE = '65000030'

def main():
    source_file = None
    for p in source_paths:
        if os.path.isfile(p):
            source_file = p
            break

    if not source_file:
        print('找不到來源檔案，請確認以下任一位置存在：')
        for p in source_paths:
            print('  -', p)
        return

    try:
        print('Reading source file...')
        try:
            df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(source_file, encoding='cp950', low_memory=False)

        # 篩選中和區（依序嘗試：行政區、district、areacode）
        if '行政區' in df.columns:
            zhonghe_df = df[df['行政區'] == '中和區'].copy()
        elif 'district' in df.columns:
            zhonghe_df = df[df['district'] == '中和區'].copy()
        elif 'areacode' in df.columns:
            zhonghe_df = df[df['areacode'].astype(str).str.strip() == ZHONGHE_AREACODE].copy()
        else:
            print('欄位內容：', list(df.columns))
            raise ValueError('找不到可篩選中和區的欄位（行政區 / district / areacode）')

        if len(zhonghe_df) == 0 and 'areacode' in df.columns:
            # 嘗試其他可能的 areacode
            codes = df['areacode'].astype(str).unique()
            zhonghe_codes = [c for c in codes if '6500003' in c or '6500300' in c]
            if zhonghe_codes:
                zhonghe_df = df[df['areacode'].astype(str).isin(zhonghe_codes)].copy()
                print('使用 areacode', zhonghe_codes, '篩選')

        if len(zhonghe_df) == 0:
            raise ValueError('篩選後無資料，請確認來源檔案包含中和區（行政區或 areacode）')

        # 確保有「行政區」欄位
        if '行政區' not in zhonghe_df.columns:
            zhonghe_df.insert(0, '行政區', '中和區')
        else:
            zhonghe_df['行政區'] = '中和區'

        # 對應 路名、巷、弄 欄位（政府門牌檔常用 street、road、section / lane / alley）
        road_col = None
        for c in zhonghe_df.columns:
            if c in ('road', '路名', '路名稱', 'roadname'):
                road_col = c
                break
            if 'road' in c.lower() or 'street' in c.lower() or '路' in c:
                road_col = c
                break
        lane_col = next((c for c in ['lane', '巷', '巷弄'] if c in zhonghe_df.columns), None)
        alley_col = next((c for c in ['alley', '弄'] if c in zhonghe_df.columns), None)

        if not road_col or not lane_col or not alley_col:
            raise ValueError('找不到路名/巷/弄欄位，現有欄位: ' + str(list(zhonghe_df.columns)))

        zhonghe_out = zhonghe_df[['行政區', road_col, lane_col, alley_col]].copy()
        zhonghe_out = zhonghe_out.rename(columns={road_col: '路名', lane_col: '巷', alley_col: '弄'})
        before = len(zhonghe_out)
        zhonghe_out = zhonghe_out.drop_duplicates()
        print('Removed', before - len(zhonghe_out), 'duplicates.')
        zhonghe_out.to_csv(output_file, index=False, encoding='utf-8-sig')

        print('Success!', len(zhonghe_out), 'unique records for Zhonghe district.')
        print('Saved to:', output_file)

    except Exception as e:
        print(f'發生錯誤：{e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
