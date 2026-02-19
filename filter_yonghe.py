# -*- coding: utf-8 -*-
"""
從桌面上新北市資料夾的「新北市門牌位置數值資料」CSV 篩選永和區，
輸出：永和區門牌位置數值資料.csv（完整欄位）、yonghe_real_data.csv（路巷弄給 server 用）
"""
import pandas as pd
import os

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

# 可能的來源路徑
source_paths = [
    os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '板橋', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '板橋區', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
]

base_dir = os.path.dirname(os.path.abspath(__file__))
output_full = os.path.join(base_dir, '永和區門牌位置數值資料.csv')
output_simple = os.path.join(base_dir, 'yonghe_real_data.csv')

# 永和區 areacode（新北市門牌位置數值資料）
YONGHE_AREACODE = '65000040'


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
        print('讀取來源檔案...', source_file)
        try:
            df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(source_file, encoding='cp950', low_memory=False)

        # 篩選永和區（依序嘗試：行政區、district、areacode）
        if '行政區' in df.columns:
            yonghe_df = df[df['行政區'] == '永和區'].copy()
        elif 'district' in df.columns:
            yonghe_df = df[df['district'] == '永和區'].copy()
        elif 'areacode' in df.columns:
            yonghe_df = df[df['areacode'].astype(str).str.strip() == YONGHE_AREACODE].copy()
        else:
            print('欄位：', list(df.columns))
            raise ValueError('找不到可篩選永和區的欄位（行政區 / district / areacode）')

        if len(yonghe_df) == 0 and 'areacode' in df.columns:
            codes = df['areacode'].astype(str).unique()
            yonghe_codes = [c for c in codes if '6500004' in c or '6500400' in c]
            if yonghe_codes:
                yonghe_df = df[df['areacode'].astype(str).isin(yonghe_codes)].copy()
                print('使用 areacode', yonghe_codes, '篩選')

        if len(yonghe_df) == 0:
            raise ValueError('篩選後無資料，請確認來源檔案包含永和區（areacode 65000040）')

        # 1) 完整門牌位置數值資料（保留所有欄位）
        yonghe_df.to_csv(output_full, index=False, encoding='utf-8-sig')
        print('已寫入完整門牌資料：', output_full)
        print('  筆數：', len(yonghe_df))

        # 2) 簡化版：行政區、路名、巷、弄（去重，給 server 用）
        road_col = None
        for c in yonghe_df.columns:
            if 'street' in c.lower() or 'road' in c.lower() or '路' in c or 'section' in c.lower():
                road_col = c
                break
        lane_col = next((c for c in ['lane', '巷', '巷弄'] if c in yonghe_df.columns), None)
        alley_col = next((c for c in ['alley', '弄'] if c in yonghe_df.columns), None)

        if road_col and lane_col is not None and alley_col is not None:
            simple = yonghe_df[[road_col, lane_col, alley_col]].copy()
            simple.insert(0, '行政區', '永和區')
            simple = simple.rename(columns={road_col: '路名', lane_col: '巷', alley_col: '弄'})
            simple = simple[['行政區', '路名', '巷', '弄']].drop_duplicates()
            simple.to_csv(output_simple, index=False, encoding='utf-8-sig')
            print('已寫入路巷弄簡表：', output_simple)
            print('  筆數：', len(simple))
        else:
            print('未產生 yonghe_real_data.csv（缺少路名/巷/弄欄位）')

    except Exception as e:
        print('發生錯誤：', e)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
