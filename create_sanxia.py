# -*- coding: utf-8 -*-
"""
從桌面上新北市資料夾的「新北市門牌位置數值資料」CSV 篩選三峽區（areacode = 65000090），
如果原始檔案中沒有該代碼，則建立空的三峽區檔案結構
"""
import pandas as pd
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 桌面路徑與新北市資料夾內的原始檔案
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_file = os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv')
# 輸出到專案目錄
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '三峽區門牌位置數值資料.csv')

try:
    print("正在讀取大型 CSV 檔案，請稍候...")
    
    # 讀取 CSV，政府檔案常見編碼為 utf-8 或 cp950
    try:
        df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(source_file, encoding='cp950', low_memory=False)
    
    print(f"原始檔案共有 {len(df)} 筆資料")
    print(f"欄位：{list(df.columns)}")
    
    # 檢查檔案中所有的 areacode
    unique_areacodes = df['areacode'].unique()
    print(f"\n檔案中的 areacode：{sorted(unique_areacodes)}")
    
    # 篩選三峽區（areacode = 65000090）
    sanxia_df = df[df['areacode'].astype(str).str.strip() == '65000090'].copy()
    
    if len(sanxia_df) == 0:
        print("\n警告：原始檔案中沒有 areacode 65000090（三峽區）的資料")
        print("將建立空的三峽區檔案結構...")
        # 建立空的 DataFrame，但保持相同的欄位結構
        sanxia_df = pd.DataFrame(columns=df.columns)
        # 確保有 areacode 和行政區欄位
        if 'areacode' not in sanxia_df.columns:
            sanxia_df['areacode'] = None
        if '行政區' not in sanxia_df.columns:
            sanxia_df['行政區'] = None
    else:
        print(f"\n找到 {len(sanxia_df)} 筆三峽區資料")
    
    # 確保有「行政區」欄位並設定為「三峽區」
    if '行政區' not in sanxia_df.columns:
        # 找到路名欄位的位置
        road_col_idx = None
        for idx, col in enumerate(sanxia_df.columns):
            if col in ['路名', 'road', 'Road', 'street', 'Street']:
                road_col_idx = idx
                break
        if road_col_idx is not None:
            sanxia_df.insert(road_col_idx, '行政區', '三峽區')
        else:
            sanxia_df.insert(1, '行政區', '三峽區')
    else:
        sanxia_df['行政區'] = '三峽區'
    
    # 確保 areacode 欄位為 65000090
    if 'areacode' in sanxia_df.columns:
        sanxia_df['areacode'] = '65000090'
    
    # 刪除重複資料
    print("正在刪除重複資料...")
    before_dedup = len(sanxia_df)
    sanxia_df = sanxia_df.drop_duplicates()
    after_dedup = len(sanxia_df)
    print(f"刪除重複後：{before_dedup} → {after_dedup} 筆")
    
    # 重新排列：先按行政區，再按路名，再按巷，再按弄
    print("正在重新排列資料...")
    sort_columns = []
    if '行政區' in sanxia_df.columns:
        sort_columns.append('行政區')
    if '路名' in sanxia_df.columns:
        sort_columns.append('路名')
    elif 'road' in sanxia_df.columns:
        sort_columns.append('road')
    if '巷' in sanxia_df.columns:
        sort_columns.append('巷')
    elif 'lane' in sanxia_df.columns:
        sort_columns.append('lane')
    if '弄' in sanxia_df.columns:
        sort_columns.append('弄')
    elif 'alley' in sanxia_df.columns:
        sort_columns.append('alley')
    
    if sort_columns and len(sanxia_df) > 0:
        sanxia_df = sanxia_df.sort_values(by=sort_columns, na_position='last')
    
    # 確保欄位順序：areacode, 行政區, 路名, 巷, 弄
    column_order = ['areacode', '行政區', '路名', '巷', '弄']
    # 只保留存在的欄位
    column_order = [col for col in column_order if col in sanxia_df.columns]
    # 加上其他欄位
    other_cols = [col for col in sanxia_df.columns if col not in column_order]
    sanxia_df = sanxia_df[column_order + other_cols]
    
    # 匯出成新的 CSV
    sanxia_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n成功！已建立三峽區門牌資料檔案，共 {len(sanxia_df)} 筆資料。")
    print(f"檔案已儲存為：{output_file}")

except FileNotFoundError as e:
    print(f"找不到檔案：{e}")
    print("建議檢查：1. 桌面是否有「新北市」資料夾 2. 資料夾內是否有「新北市門牌位置數值資料.csv」")
except Exception as e:
    print(f"發生錯誤：{e}")
    import traceback
    traceback.print_exc()
