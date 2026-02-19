# -*- coding: utf-8 -*-
"""
從桌面上板橋資料夾的「新北市門牌位置數值資料」CSV 篩選板橋區，輸出為 banqiao_real_data.csv
"""
import pandas as pd
import os

# 桌面路徑與板橋資料夾內的原始檔案
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_file = os.path.join(desktop, '板橋', '新北市門牌位置數值資料.csv')
# 輸出到專案目錄，方便 server 使用
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'banqiao_real_data.csv')

try:
    print("正在讀取大型 CSV 檔案，請稍候...")
    
    # 讀取 CSV，政府檔案常見編碼為 utf-8 或 cp950
    try:
        df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(source_file, encoding='cp950', low_memory=False)

    # 政府門牌資料沒有 district 欄位，改用 areacode（板橋區 = 65000010）
    if 'district' in df.columns:
        banqiao_df = df[df['district'] == '板橋區']
    elif '行政區' in df.columns:
        banqiao_df = df[df['行政區'] == '板橋區']
    elif 'areacode' in df.columns:
        banqiao_df = df[df['areacode'].astype(str) == '65000010']
    else:
        raise ValueError("找不到可篩選板橋區的欄位（district / 行政區 / areacode）")

    # 在路名欄位前新增「行政區」欄位（板橋區）
    if '行政區' not in banqiao_df.columns:
        banqiao_df.insert(2, '行政區', '板橋區')

    # 刪除 countycode、areacode 兩欄（板橋區資料固定為 65000、65000010，不需保留）
    banqiao_df = banqiao_df.drop(columns=['countycode', 'areacode'], errors='ignore')
    # 刪除座標欄位 x_3826、y_3826
    banqiao_df = banqiao_df.drop(columns=['x_3826', 'y_3826'], errors='ignore')

    # 匯出成新的 CSV
    banqiao_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"成功！已從原始檔案中篩選出 {len(banqiao_df)} 筆板橋區資料。")
    print(f"檔案已儲存為：{output_file}")

except Exception as e:
    print(f"發生錯誤：{e}")
    print("建議檢查：1. 桌面是否有「板橋」資料夾 2. 資料夾內是否有「新北市門牌位置數值資料.csv」 3. 原始檔案的編碼格式")
