# -*- coding: utf-8 -*-
"""
從台北市原始門牌資料中提取大同區資料
參考中正區的格式，從完整的台北市資料中篩選大同區
"""

import csv
import os
import sys
import io

# 設定輸出編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 可能的台北市原始資料來源
possible_sources = [
    r'c:\Users\user\Desktop\台北市\台北市門牌位置數值資料.csv',
    r'c:\Users\user\Desktop\台北市\台北市門牌位置數值資料.CSV',
    r'c:\Users\user\Desktop\taipei\台北市門牌位置數值資料.csv',
    r'c:\Users\user\Desktop\taipei\台北市門牌位置數值資料.CSV',
    r'c:\Users\user\Desktop\台北市門牌位置數值資料.csv',
    r'c:\Users\user\Desktop\台北市門牌位置數值資料.CSV',
]

output_path = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料.CSV'

# 尋找原始資料檔案
source_file = None
for path in possible_sources:
    if os.path.exists(path):
        source_file = path
        print(f'找到原始資料: {source_file}')
        break

if not source_file:
    print('找不到原始台北市門牌資料檔案')
    print('\n請確認以下位置之一存在檔案:')
    for p in possible_sources:
        print(f'  - {p}')
    print('\n或者請提供原始資料檔案路徑')
    print('\n提示：如果檔案在其他位置，請修改腳本中的 possible_sources 列表')
    sys.exit(1)

# 嘗試不同編碼讀取
encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950']

content = None
used_encoding = None

for encoding in encodings:
    try:
        with open(source_file, 'r', encoding=encoding) as f:
            test_content = f.read()
        # 檢查是否包含關鍵字
        if '區名' in test_content and '街路段' in test_content:
            content = test_content
            used_encoding = encoding
            print(f'成功使用編碼: {encoding}')
            break
    except Exception as e:
        continue

if not content:
    print('無法讀取檔案，請檢查檔案編碼')
    sys.exit(1)

# 解析 CSV
lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
lines = [l for l in lines if l.strip()]

if len(lines) < 2:
    print('檔案格式錯誤：資料行數不足')
    sys.exit(1)

# 解析表頭
header_row = lines[0].replace('\ufeff', '').strip()

# 判斷分隔符（台北市格式通常是逗號）
if '\t' in header_row:
    delimiter = '\t'
    print('使用 Tab 分隔符')
else:
    delimiter = ','
    print('使用逗號分隔符')

headers = header_row.split(delimiter)
print(f'欄位數: {len(headers)}')
print(f'欄位名稱: {headers}')

# 找到關鍵欄位索引
idx_district = None
idx_road = None
idx_lane = None
idx_alley = None

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

# 如果找不到，使用位置推斷（通常：省市,鄉鎮,區名(2),村里(3),鄰(4),街路段(5),地區(6),巷(7),弄(8),號(9)）
if idx_district is None:
    if len(headers) >= 3:
        idx_district = 2  # 第 3 欄
        print('使用位置推斷：區名在第 3 欄')
if idx_road is None:
    if len(headers) >= 6:
        idx_road = 5  # 第 6 欄
        print('使用位置推斷：街路段在第 6 欄')
if idx_lane is None:
    if len(headers) >= 8:
        idx_lane = 7  # 第 8 欄
if idx_alley is None:
    if len(headers) >= 9:
        idx_alley = 8  # 第 9 欄

if idx_district is None or idx_road is None:
    print(f'錯誤：無法找到必要欄位')
    print(f'區名索引: {idx_district}, 路名索引: {idx_road}')
    print(f'所有欄位: {headers}')
    sys.exit(1)

print(f'\n欄位索引:')
print(f'  區名: {idx_district} ({headers[idx_district] if idx_district < len(headers) else "N/A"})')
print(f'  路名: {idx_road} ({headers[idx_road] if idx_road < len(headers) else "N/A"})')
print(f'  巷: {idx_lane}')
print(f'  弄: {idx_alley}')

# 篩選大同區資料
seen = set()
rows = []
datong_count = 0
total_count = 0

for i, line in enumerate(lines[1:], 1):
    if not line.strip():
        continue
    
    total_count += 1
    cols = line.split(delimiter)
    
    if len(cols) <= max(idx_district, idx_road):
        continue
    
    district = (cols[idx_district] if idx_district < len(cols) else '').strip()
    
    # 篩選大同區
    if district != '大同區':
        continue
    
    datong_count += 1
    road = (cols[idx_road] if idx_road < len(cols) else '').strip()
    lane = (cols[idx_lane] if idx_lane is not None and idx_lane < len(cols) else '').strip()
    alley = (cols[idx_alley] if idx_alley is not None and idx_alley < len(cols) else '').strip()
    
    if not road:
        continue
    
    # 建立輸出列（格式：areacode,行政區,路名,巷,弄）
    output_row = ['', '大同區', road, lane, alley]
    
    # 去重（以 路名, 巷, 弄 為 key）
    key = (road, lane, alley)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)

print(f'\n處理結果:')
print(f'  總筆數: {total_count}')
print(f'  大同區筆數: {datong_count}')
print(f'  去重後筆數: {len(rows)}')

if len(rows) == 0:
    print('\n警告：沒有找到大同區資料')
    print('請確認原始檔案中包含「大同區」的資料')
    sys.exit(1)

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))  # 依 路名, 巷, 弄 排序

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄']

# 備份原檔案
backup_file = output_path + '.backup'
if os.path.exists(output_path) and not os.path.exists(backup_file):
    import shutil
    shutil.copy2(output_path, backup_file)
    print(f'\n已備份原檔案為: {backup_file}')

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'\n完成！已寫入: {output_path}')
print(f'共 {len(rows)} 筆不重複門牌資料')
print(f'\n前 10 筆資料:')
for i, row in enumerate(rows[:10], 1):
    print(f'  {i}. {row}')
