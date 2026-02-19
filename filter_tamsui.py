# -*- coding: utf-8 -*-
"""
從桌面上新北市資料夾的「新北市門牌位置數值資料」CSV 篩選淡水區，輸出為淡水區門牌位置數值資料.csv
"""
import pandas as pd
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 桌面路徑與新北市資料夾內的原始檔案
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_file = os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv')
# 輸出到專案目錄
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '淡水區門牌位置數值資料.csv')

TAMSUI_AREACODE = '65000100'

try:
    print("正在讀取大型 CSV 檔案，請稍候...")
    
    # 讀取 CSV，政府檔案常見編碼為 utf-8 或 cp950
    try:
        df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(source_file, encoding='cp950', low_memory=False)

    print(f"原始資料總筆數: {len(df)}")
    
    # 篩選淡水區（areacode = 65000100）
    tamsui_df = df[df['areacode'].astype(str).str.strip() == TAMSUI_AREACODE].copy()
    
    print(f"淡水區資料筆數: {len(tamsui_df)}")
    
    if len(tamsui_df) == 0:
        raise ValueError('篩選後無資料，請確認來源檔案包含淡水區（areacode = 65000100）')

    # 準備輸出格式：areacode,行政區,路名,巷,弄
    # 需要從原始欄位對應到目標欄位
    # 原始欄位：street、road、section -> 路名
    # lane -> 巷
    # alley -> 弄
    
    # 合併路名欄位（street、road、section）
    road_cols = []
    if 'street、road、section' in tamsui_df.columns:
        road_cols.append('street、road、section')
    elif 'street' in tamsui_df.columns:
        road_cols.append('street')
    if 'road' in tamsui_df.columns and 'road' not in road_cols:
        road_cols.append('road')
    if 'section' in tamsui_df.columns:
        road_cols.append('section')
    
    # 建立路名字串
    if road_cols:
        tamsui_df['路名'] = tamsui_df[road_cols].fillna('').astype(str).apply(
            lambda x: ''.join([str(v) for v in x if pd.notna(v) and str(v).strip() != '']), axis=1
        )
    else:
        # 如果找不到路名欄位，嘗試其他可能的欄位名稱
        possible_road_cols = [col for col in tamsui_df.columns if '路' in col or '街' in col or 'road' in col.lower() or 'street' in col.lower()]
        if possible_road_cols:
            tamsui_df['路名'] = tamsui_df[possible_road_cols[0]].fillna('').astype(str)
        else:
            tamsui_df['路名'] = ''
    
    # 處理巷欄位
    if 'lane' in tamsui_df.columns:
        tamsui_df['巷'] = tamsui_df['lane'].fillna('').astype(str)
    else:
        tamsui_df['巷'] = ''
    
    # 處理弄欄位
    if 'alley' in tamsui_df.columns:
        tamsui_df['弄'] = tamsui_df['alley'].fillna('').astype(str)
    else:
        tamsui_df['弄'] = ''
    
    # 建立輸出資料框
    output_df = pd.DataFrame({
        'areacode': TAMSUI_AREACODE,
        '行政區': '淡水區',
        '路名': tamsui_df['路名'],
        '巷': tamsui_df['巷'],
        '弄': tamsui_df['弄']
    })
    
    # 清理空白值
    output_df['路名'] = output_df['路名'].str.strip()
    output_df['巷'] = output_df['巷'].str.strip()
    output_df['弄'] = output_df['弄'].str.strip()
    
    # 刪除重複資料
    print(f"去重前筆數: {len(output_df)}")
    output_df = output_df.drop_duplicates()
    print(f"去重後筆數: {len(output_df)}")
    
    # 重新排列：先按路名，再按巷，再按弄
    output_df = output_df.sort_values(by=['路名', '巷', '弄'], na_position='last')
    
    # 重置索引
    output_df = output_df.reset_index(drop=True)
    
    # 匯出成新的 CSV
    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"成功！已從原始檔案中篩選出 {len(output_df)} 筆淡水區門牌資料")
    print(f"輸出檔案：{output_file}")
    
except FileNotFoundError:
    print(f"錯誤：找不到來源檔案 {source_file}")
    print("請確認檔案路徑正確")
except Exception as e:
    print(f"發生錯誤：{str(e)}")
    import traceback
    traceback.print_exc()
