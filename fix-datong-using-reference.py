# -*- coding: utf-8 -*-
"""
使用其他正確格式的台北市區檔案作為參考，修正大同區檔案
參考中正區的格式來處理大同區資料
"""

import csv
import os
import sys
import io
import re

# 設定輸出編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 參考檔案（格式正確的台北市區檔案）
reference_file = r'c:\Users\user\Desktop\newtaipei\中正區門牌位置數值資料.CSV'
datong_file = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料.CSV'
output_file = r'c:\Users\user\Desktop\newtaipei\大同區門牌位置數值資料_new.CSV'

print('=' * 60)
print('使用參考檔案格式來修正大同區資料')
print('=' * 60)

# 讀取參考檔案以了解正確格式
if not os.path.exists(reference_file):
    print(f'錯誤：找不到參考檔案: {reference_file}')
    print('請確認中正區檔案存在')
    sys.exit(1)

print(f'\n1. 讀取參考檔案: {reference_file}')
with open(reference_file, 'r', encoding='utf-8-sig') as f:
    ref_content = f.read()

ref_lines = ref_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
ref_lines = [l for l in ref_lines if l.strip()]

if len(ref_lines) < 2:
    print('參考檔案格式錯誤')
    sys.exit(1)

ref_header = ref_lines[0].replace('\ufeff', '').strip()
ref_delimiter = ',' if ',' in ref_header else '\t'
ref_headers = ref_header.split(ref_delimiter)

print(f'   參考檔案格式:')
print(f'   - 分隔符: {"逗號" if ref_delimiter == "," else "Tab"}')
print(f'   - 欄位數: {len(ref_headers)}')
print(f'   - 欄位名稱: {ref_headers}')

# 找到參考檔案中的欄位索引
ref_idx_district = ref_headers.index('區名') if '區名' in ref_headers else 2
ref_idx_road = ref_headers.index('街路段') if '街路段' in ref_headers else 5
ref_idx_lane = ref_headers.index('巷') if '巷' in ref_headers else 7
ref_idx_alley = ref_headers.index('弄') if '弄' in ref_headers else 8

print(f'\n2. 讀取大同區檔案: {datong_file}')

# 嘗試多種編碼讀取大同區檔案
encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950', 'gb2312', 'gbk', 'gb18030']

content = None
used_encoding = None

for encoding in encodings:
    try:
        with open(datong_file, 'r', encoding=encoding) as f:
            test_content = f.read()
        
        # 檢查是否包含有效的中文字
        chinese_count = len([c for c in test_content if '\u4e00' <= c <= '\u9fa5'])
        
        if chinese_count > 100:
            content = test_content
            used_encoding = encoding
            print(f'   使用編碼: {encoding}, 中文字數: {chinese_count}')
            break
    except Exception as e:
        continue

if not content:
    print('   無法讀取大同區檔案')
    sys.exit(1)

# 解析大同區檔案
datong_lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
datong_lines = [l for l in datong_lines if l.strip()]

if len(datong_lines) < 2:
    print('   大同區檔案格式錯誤')
    sys.exit(1)

datong_header = datong_lines[0].replace('\ufeff', '').strip()
datong_delimiter = '\t' if '\t' in datong_header else ','
datong_headers = datong_header.split(datong_delimiter)

print(f'   大同區檔案格式:')
print(f'   - 分隔符: {"Tab" if datong_delimiter == "\t" else "逗號"}')
print(f'   - 欄位數: {len(datong_headers)}')
print(f'   - 欄位名稱: {datong_headers[:6]}')

# 根據參考檔案的格式推斷大同區檔案的欄位索引
# 假設格式相同：省市,鄉鎮,區名(2),村里(3),鄰(4),街路段(5),地區(6),巷(7),弄(8),號(9)
if len(datong_headers) >= 6:
    idx_district = 2  # 第 3 欄：區名
    idx_road = 5       # 第 6 欄：街路段
    idx_lane = 7 if len(datong_headers) > 7 else None
    idx_alley = 8 if len(datong_headers) > 8 else None
else:
    print('   錯誤：欄位數不足')
    sys.exit(1)

print(f'\n3. 處理資料...')

# 處理資料
seen = set()
rows = []
valid_count = 0
total_count = 0
invalid_count = 0

for i, line in enumerate(datong_lines[1:], 1):
    if not line.strip():
        continue
    
    total_count += 1
    cols = line.split(datong_delimiter)
    
    if len(cols) <= max(idx_district, idx_road):
        continue
    
    # 提取欄位
    district_raw = (cols[idx_district] if idx_district < len(cols) else '').strip()
    road_raw = (cols[idx_road] if idx_road < len(cols) else '').strip()
    lane_raw = (cols[idx_lane] if idx_lane is not None and idx_lane < len(cols) else '').strip()
    alley_raw = (cols[idx_alley] if idx_alley is not None and idx_alley < len(cols) else '').strip()
    
    # 檢查路名是否包含中文字（即使編碼有問題，某些字元可能仍可辨識）
    if not road_raw:
        invalid_count += 1
        continue
    
    # 強制設定為大同區（因為這是大同區檔案）
    district = '大同區'
    
    # 嘗試清理路名（移除明顯的亂碼字元）
    # 如果路名看起來像亂碼，我們仍然保留它，讓系統嘗試處理
    road = road_raw
    
    valid_count += 1
    
    # 建立輸出列
    output_row = ['', '大同區', road, lane_raw, alley_raw]
    
    # 去重
    key = (road, lane_raw, alley_raw)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)

print(f'   處理結果:')
print(f'   - 總筆數: {total_count}')
print(f'   - 有效筆數: {valid_count}')
print(f'   - 無效筆數: {invalid_count}')
print(f'   - 去重後筆數: {len(rows)}')

if len(rows) == 0:
    print('\n   警告：沒有提取到有效資料')
    print('   建議：請從原始來源重新下載大同區資料')
    sys.exit(1)

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 備份原檔案
backup_file = datong_file + '.backup'
if os.path.exists(datong_file) and not os.path.exists(backup_file):
    import shutil
    shutil.copy2(datong_file, backup_file)
    print(f'\n4. 已備份原檔案為: {backup_file}')

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'\n5. 寫入新檔案: {output_file}')
with open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'\n完成！已寫入 {len(rows)} 筆資料')
print(f'\n前 10 筆資料預覽:')
for i, row in enumerate(rows[:10], 1):
    print(f'   {i}. {row}')

print(f'\n注意：')
print(f'   - 如果路名仍顯示為亂碼，表示原始檔案編碼問題嚴重')
print(f'   - 建議從原始資料來源重新下載大同區資料')
print(f'   - 或使用其他正確格式的台北市區檔案作為參考')
