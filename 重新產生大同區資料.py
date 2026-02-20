# -*- coding: utf-8 -*-
"""
重新產生大同區門牌位置數值資料
從原始台北市門牌資料中篩選大同區，轉換為正確格式
"""

import csv
import os
import sys

# 可能的原始資料來源
possible_sources = [
    r'c:\Users\user\Desktop\台北市\台北市門牌位置數值資料.csv',
    r'c:\Users\user\Desktop\台北市\台北市門牌位置數值資料.CSV',
    r'c:\Users\user\Desktop\taipei\台北市門牌位置數值資料.csv',
    r'c:\Users\user\Desktop\taipei\台北市門牌位置數值資料.CSV',
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
    print('請確認以下位置之一存在檔案:')
    for p in possible_sources:
        print(f'  - {p}')
    print('\n或者請提供原始資料檔案路徑')
    sys.exit(1)

# 嘗試不同編碼讀取
encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950', 'gb2312', 'gbk']

content = None
used_encoding = None

for encoding in encodings:
    try:
        with open(source_file, 'r', encoding=encoding) as f:
            content = f.read()
        # 檢查是否包含關鍵字
        if '區名' in content or '街路段' in content or '大同區' in content:
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

# 判斷分隔符
if '\t' in header_row:
    delimiter = '\t'
    print('使用 Tab 分隔符')
else:
    delimiter = ','
    print('使用逗號分隔符')

headers = header_row.split(delimiter)
print(f'欄位數: {len(headers)}')
print(f'欄位名稱: {headers[:10]}')

# 找到關鍵欄位索引
idx_district = None
idx_road = None
idx_lane = None
idx_alley = None
idx_number = None

for i, h in enumerate(headers):
    h_clean = h.strip()
    if h_clean == '區名' or '區名' in h_clean or h_clean == '鄉鎮市區':
        idx_district = i
    elif h_clean == '街路段' or '街路段' in h_clean or h_clean == '路名':
        idx_road = i
    elif h_clean == '巷' or '巷' in h_clean:
        idx_lane = i
    elif h_clean == '弄' or '弄' in h_clean:
        idx_alley = i
    elif h_clean == '號' or '號' in h_clean:
        idx_number = i

# 如果找不到，使用位置推斷（通常：省市,鄉鎮,區名,村里,鄰,街路段,地區,巷,弄,號）
if idx_district is None:
    if len(headers) >= 3:
        idx_district = 2  # 第 3 欄
        print('使用位置推斷：區名在第 3 欄')
if idx_road is None:
    if len(headers) >= 6:
        idx_road = 5  # 第 6 欄
        print('使用位置推斷：街路段在第 6 欄')

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
print(f'  號: {idx_number}')

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
    
    district = (cols[idx_district] || '').strip()
    
    # 篩選大同區
    if district != '大同區':
        continue
    
    datong_count += 1
    road = (cols[idx_road] || '').strip()
    lane = (cols[idx_lane] if idx_lane is not None and idx_lane < len(cols) else '').strip()
    alley = (cols[idx_alley] if idx_alley is not None and idx_alley < len(cols) else '').strip()
    number = (cols[idx_number] if idx_number is not None and idx_number < len(cols) else '').strip()
    
    if not road:
        continue
    
    # 建立輸出列（格式：areacode,行政區,路名,巷,弄）
    # 台北市格式通常沒有 areacode，使用空值或區名代碼
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

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))  # 依 路名, 巷, 弄 排序

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄']

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'\n完成！已寫入: {output_path}')
print(f'共 {len(rows)} 筆不重複門牌資料')
