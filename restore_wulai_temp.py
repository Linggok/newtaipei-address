# -*- coding: utf-8 -*-
"""復原烏來區檔案，寫入臨時檔案"""
import csv
import os
import sys
import shutil

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
temp_path = os.path.join(base_dir, '烏來區門牌位置數值資料_temp.csv')
output_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

# 可能的來源路徑
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_paths = [
    os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
]

# 烏來區代碼
WULAI_AREACODE = '65000290'

# 要添加的路名
new_roads = [
    ('大羅蘭', '', ''),
    ('天仁', '', ''),
    ('屯鹿', '', ''),
    ('卡拉模基', '', ''),
    ('李茂岸', '', ''),
    ('忠治', '', ''),
    ('金堰', '', ''),
    ('金堰', '１１５巷', ''),
    ('娃娃谷', '', ''),
    ('紅河', '', ''),
    ('馬岸', '', ''),
    ('桶後', '', ''),
    ('瀑布', '', ''),
]

# 找到來源檔案
input_path = None
for path in source_paths:
    if os.path.exists(path):
        input_path = path
        print(f'找到來源檔案: {input_path}')
        break

if not input_path:
    print('錯誤：找不到新北市門牌位置數值資料.csv')
    exit(1)

# 讀取並處理資料
seen = set()
rows = []

try:
    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        print(f'成功讀取檔案')
        
        for row in reader:
            if len(row) >= 2 and row[1] == WULAI_AREACODE:
                areacode = row[1] if len(row) > 1 else ''
                road = row[4] if len(row) > 4 else ''
                lane = row[6] if len(row) > 6 else ''
                alley = row[7] if len(row) > 7 else ''
                
                output_row = [areacode, '烏來區', road, lane, alley]
                key = (road.strip(), lane.strip(), alley.strip())
                if key not in seen:
                    seen.add(key)
                    rows.append(output_row)
        
        print(f'從原始資料讀取 {len(rows)} 筆')

except Exception as e:
    print(f'發生錯誤: {e}')
    exit(1)

# 添加新路名
print('\n添加新路名...')
for road, lane, alley in new_roads:
    output_row = ['65000290', '烏來區', road, lane, alley]
    key = (road, lane, alley)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)
        print(f'  已添加: {road}, {lane}, {alley}')

# 排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'\n寫入臨時檔案: {temp_path}')
with open(temp_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'完成！已生成臨時檔案，共 {len(rows)} 筆資料')
print(f'檔案格式: {output_header}')
print(f'\n請手動將 {temp_path} 重新命名為 {output_path}')
print('或關閉 Cursor 後執行以下命令:')
print(f'  move "{temp_path}" "{output_path}"')
