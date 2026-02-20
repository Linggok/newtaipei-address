# -*- coding: utf-8 -*-
"""
從現有的大同區檔案重新產生正確格式的資料
根據實際檔案格式調整
"""

import csv
import os
import sys
import io
import re

# 設定輸出編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

input_file = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料.CSV'
output_file = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料_fixed.CSV'

# 如果已經有轉換後的檔案，使用它
if os.path.exists(r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料_utf8.CSV'):
    input_file = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料_utf8.CSV'
    print('使用已轉換的檔案:', input_file)

print(f'讀取檔案: {input_file}')

# 嘗試多種編碼
encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950', 'gb2312', 'gbk', 'gb18030']

content = None
used_encoding = None

for encoding in encodings:
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            test_content = f.read()
        
        # 檢查是否包含有效的中文字
        chinese_count = len([c for c in test_content if '\u4e00' <= c <= '\u9fa5'])
        
        if chinese_count > 100:  # 至少要有一些中文字
            content = test_content
            used_encoding = encoding
            print(f'使用編碼: {encoding}, 中文字數: {chinese_count}')
            break
    except Exception as e:
        continue

if not content:
    print('無法讀取檔案')
    sys.exit(1)

# 解析 CSV
lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
lines = [l for l in lines if l.strip()]

if len(lines) < 2:
    print('檔案格式錯誤')
    sys.exit(1)

# 判斷分隔符
header_row = lines[0].replace('\ufeff', '').strip()
if '\t' in header_row:
    delimiter = '\t'
    print('使用 Tab 分隔符')
else:
    delimiter = ','
    print('使用逗號分隔符')

headers = header_row.split(delimiter)
print(f'欄位數: {len(headers)}')
print(f'欄位名稱: {headers}')

# 檢查實際資料行的欄位數
sample_line = lines[1] if len(lines) > 1 else ''
sample_cols = sample_line.split(delimiter)
print(f'樣本資料欄位數: {len(sample_cols)}')
print(f'樣本資料前 6 欄: {sample_cols[:6]}')

# 根據實際欄位數調整索引
# 如果只有 6 個欄位，可能是：省市,鄉鎮,區名,村里,鄰,街路段（簡化版）
if len(headers) == 6:
    idx_district = 2  # 第 3 欄：區名
    idx_road = 5      # 第 6 欄：街路段
    idx_lane = None   # 可能沒有
    idx_alley = None
    idx_number = None
    print('\n偵測到簡化格式（6 欄位）')
elif len(headers) >= 10:
    idx_district = 2  # 第 3 欄
    idx_road = 5      # 第 6 欄
    idx_lane = 7      # 第 8 欄
    idx_alley = 8     # 第 9 欄
    idx_number = 9    # 第 10 欄
    print('\n偵測到完整格式（10+ 欄位）')
else:
    # 嘗試推斷
    idx_district = 2 if len(headers) > 2 else None
    idx_road = min(5, len(headers) - 1) if len(headers) > 5 else None
    idx_lane = None
    idx_alley = None
    idx_number = None
    print(f'\n使用推斷格式（{len(headers)} 欄位）')

print(f'\n欄位索引:')
print(f'  區名: {idx_district}')
print(f'  路名: {idx_road}')
print(f'  巷: {idx_lane}')
print(f'  弄: {idx_alley}')
print(f'  號: {idx_number}')

# 處理資料
seen = set()
rows = []
valid_count = 0
total_count = 0

for i, line in enumerate(lines[1:], 1):
    if not line.strip():
        continue
    
    total_count += 1
    cols = line.split(delimiter)
    
    if len(cols) <= max(idx_district or 0, idx_road or 0):
        continue
    
    # 提取欄位
    district = (cols[idx_district] if idx_district is not None and idx_district < len(cols) else '').strip()
    road = (cols[idx_road] if idx_road is not None and idx_road < len(cols) else '').strip()
    lane = (cols[idx_lane] if idx_lane is not None and idx_lane < len(cols) else '').strip()
    alley = (cols[idx_alley] if idx_alley is not None and idx_alley < len(cols) else '').strip()
    number = (cols[idx_number] if idx_number is not None and idx_number < len(cols) else '').strip()
    
    # 檢查是否為有效的中文字
    if not road or not re.search(r'[\u4e00-\u9fa5]', road):
        continue
    
    # 強制設定為大同區（因為這是大同區檔案）
    district = '大同區'
    
    valid_count += 1
    
    # 建立輸出列
    output_row = ['', '大同區', road, lane, alley]
    
    # 去重
    key = (road, lane, alley)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)

print(f'\n處理結果:')
print(f'  總筆數: {total_count}')
print(f'  有效筆數: {valid_count}')
print(f'  去重後筆數: {len(rows)}')

if len(rows) == 0:
    print('\n警告：沒有提取到有效資料')
    sys.exit(1)

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄']

with open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'\n完成！已寫入: {output_file}')
print(f'共 {len(rows)} 筆不重複門牌資料')
print(f'\n前 5 筆資料:')
for i, row in enumerate(rows[:5], 1):
    print(f'  {i}. {row}')

print(f'\n請檢查檔案內容，如果正確，可以覆蓋原檔案')
