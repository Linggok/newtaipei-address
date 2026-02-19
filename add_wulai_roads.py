# -*- coding: utf-8 -*-
"""在烏來區門牌資料中添加新的路名"""
import csv
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')
output_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

# 要添加的路名
new_roads = [
    ('大羅蘭', '', ''),
    ('天仁', '', ''),
    ('屯鹿', '', ''),
    ('卡拉模基', '', ''),
    ('李茂岸', '', ''),
    ('忠治', '', ''),
    ('金堰', '', ''),
    ('金堰', '１１５巷', ''),  # 金堰有115巷
    ('娃娃谷', '', ''),
    ('紅河', '', ''),
    ('馬岸', '', ''),
    ('桶後', '', ''),
    ('瀑布', '', ''),
]

# 讀取現有資料
rows = []
seen = set()

try:
    with open(input_path, 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        for row in reader:
            if len(row) >= 5:
                areacode = row[0].strip()
                district = row[1].strip()
                road = row[2].strip()
                lane = row[3].strip()
                alley = row[4].strip()
                
                # 建立輸出列
                output_row = [areacode, district, road, lane, alley]
                
                # 以 (路名, 巷, 弄) 去重
                key = (road, lane, alley)
                if key not in seen:
                    seen.add(key)
                    rows.append(output_row)
except Exception as e:
    print(f'讀取檔案時發生錯誤: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 添加新路名
print('添加新路名...')
for road, lane, alley in new_roads:
    output_row = ['65000290', '烏來區', road, lane, alley]
    key = (road, lane, alley)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)
        print(f'  已添加: {road}, {lane}, {alley}')

# 依 路名、巷、弄 重新排序
print('正在排序資料...')
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'寫入檔案，共 {len(rows)} 筆資料...')
with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'完成！已更新烏來區門牌資料，共 {len(rows)} 筆')
print(f'檔案已儲存為：{output_path}')
print('資料已依路名/巷/弄排序')
