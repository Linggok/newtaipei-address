# -*- coding: utf-8 -*-
"""
清理中正區門牌位置數值資料
刪除：省縣市代碼、鄉鎮市區代碼、村里、鄰、橫座標、縱座標
保留：行政區、路名、巷、弄、號
輸出格式：areacode,行政區,路名,巷,弄,號
"""

import csv
import os
import sys
import io

# 設定輸出編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 從備份檔案讀取（如果存在），否則從原檔案讀取
backup_file = r'c:\Users\user\Desktop\newtaipei\中正區門牌位置數值資料_backup.CSV'
input_file = r'c:\Users\user\Desktop\newtaipei\中正區門牌位置數值資料.CSV'
output_file = r'c:\Users\user\Desktop\newtaipei\中正區門牌位置數值資料.CSV'

print('=' * 60)
print('清理中正區門牌位置數值資料（保留號）')
print('=' * 60)

# 決定使用哪個檔案作為輸入
if os.path.exists(backup_file):
    source_file = backup_file
    print(f'\n使用備份檔案作為來源: {backup_file}')
else:
    source_file = input_file
    # 如果沒有備份，先建立備份
    if os.path.exists(input_file):
        import shutil
        shutil.copy2(input_file, backup_file)
        print(f'\n已建立備份檔案: {backup_file}')

if not os.path.exists(source_file):
    print(f'錯誤：找不到檔案: {source_file}')
    sys.exit(1)

# 讀取檔案
print(f'\n讀取檔案: {source_file}')
with open(source_file, 'r', encoding='utf-8-sig') as f:
    content = f.read()

lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
lines = [l for l in lines if l.strip()]

if len(lines) < 2:
    print('檔案格式錯誤：資料行數不足')
    sys.exit(1)

# 解析表頭
header_row = lines[0].replace('\ufeff', '').strip()
delimiter = ',' if ',' in header_row else '\t'
headers = header_row.split(delimiter)

print(f'原始欄位: {headers}')
print(f'欄位數: {len(headers)}')

# 找到要保留的欄位索引
# 原始格式：省市縣市代碼,鄉鎮市區代碼,區名,村里,鄰,街路段,地區,巷,弄,號,橫座標,縱座標
# 要刪除：省市縣市代碼(0), 鄉鎮市區代碼(1), 村里(3), 鄰(4), 地區(6), 橫座標(10), 縱座標(11)
# 要保留：區名(2), 街路段(5), 巷(7), 弄(8), 號(9)

idx_district = None  # 區名
idx_road = None      # 街路段
idx_lane = None      # 巷
idx_alley = None     # 弄
idx_number = None    # 號

for i, h in enumerate(headers):
    h_clean = h.strip()
    if h_clean == '區名':
        idx_district = i
    elif h_clean == '街路段':
        idx_road = i
    elif h_clean == '巷':
        idx_lane = i
    elif h_clean == '弄':
        idx_alley = i
    elif h_clean == '號':
        idx_number = i

# 如果找不到，使用位置推斷
if idx_district is None and len(headers) >= 3:
    idx_district = 2
if idx_road is None and len(headers) >= 6:
    idx_road = 5
if idx_lane is None and len(headers) >= 8:
    idx_lane = 7
if idx_alley is None and len(headers) >= 9:
    idx_alley = 8
if idx_number is None and len(headers) >= 10:
    idx_number = 9

print(f'\n欄位索引:')
print(f'  區名: {idx_district}')
print(f'  街路段: {idx_road}')
print(f'  巷: {idx_lane}')
print(f'  弄: {idx_alley}')
print(f'  號: {idx_number}')

if idx_district is None or idx_road is None:
    print('錯誤：無法找到必要欄位')
    sys.exit(1)

# 處理資料
print(f'\n處理資料...')
seen = set()
rows = []
total_count = 0

for i, line in enumerate(lines[1:], 1):
    if not line.strip():
        continue
    
    total_count += 1
    cols = line.split(delimiter)
    
    if len(cols) <= max(idx_district, idx_road):
        continue
    
    # 提取要保留的欄位
    district = (cols[idx_district] if idx_district is not None and idx_district < len(cols) else '').strip()
    road = (cols[idx_road] if idx_road is not None and idx_road < len(cols) else '').strip()
    lane = (cols[idx_lane] if idx_lane is not None and idx_lane < len(cols) else '').strip()
    alley = (cols[idx_alley] if idx_alley is not None and idx_alley < len(cols) else '').strip()
    number = (cols[idx_number] if idx_number is not None and idx_number < len(cols) else '').strip()
    
    if not road:
        continue
    
    # 建立輸出列（格式：areacode,行政區,路名,巷,弄,號）
    output_row = ['', district, road, lane, alley, number]
    
    # 去重（以 路名, 巷, 弄, 號 為 key）
    key = (road, lane, alley, number)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)

print(f'  總筆數: {total_count}')
print(f'  去重後筆數: {len(rows)}')

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4], r[5]))  # 依 路名, 巷, 弄, 號 排序

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄', '號']

print(f'\n寫入檔案: {output_file}')
with open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'\n完成！已寫入 {len(rows)} 筆資料')
print(f'\n前 10 筆資料預覽:')
for i, row in enumerate(rows[:10], 1):
    print(f'   {i}. {row}')

print(f'\n已刪除的欄位:')
print(f'   - 省市縣市代碼')
print(f'   - 鄉鎮市區代碼')
print(f'   - 村里')
print(f'   - 鄰')
print(f'   - 地區')
print(f'   - 橫座標')
print(f'   - 縱座標')
print(f'\n保留的欄位:')
print(f'   - 區名（行政區）')
print(f'   - 街路段（路名）')
print(f'   - 巷')
print(f'   - 弄')
print(f'   - 號')
