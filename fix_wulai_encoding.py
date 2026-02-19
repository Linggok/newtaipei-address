# -*- coding: utf-8 -*-
"""修復烏來區檔案的編碼問題"""
import csv
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

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

print(f'讀取檔案: {file_path}')

# 讀取現有資料
rows = []
seen = set()

# 嘗試不同的編碼讀取
encodings = ['utf-8-sig', 'utf-8', 'cp950', 'big5']
file_read = False

for encoding in encodings:
    try:
        with open(file_path, 'r', encoding=encoding) as infile:
            reader = csv.reader(infile)
            header = next(reader)
            print(f'成功讀取，編碼: {encoding}')
            print(f'標題: {header}')
            
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
            
            file_read = True
            print(f'已讀取 {len(rows)} 筆現有資料')
            break
    except Exception as e:
        print(f'使用編碼 {encoding} 失敗: {e}')
        continue

if not file_read:
    print('無法讀取檔案，從原始資料重新生成...')
    # 從原始資料重新生成
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    source_path = os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv')
    
    if os.path.exists(source_path):
        with open(source_path, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            
            for row in reader:
                if len(row) >= 2 and row[1] == '65000290':
                    areacode = row[1] if len(row) > 1 else ''
                    road = row[4] if len(row) > 4 else ''
                    lane = row[6] if len(row) > 6 else ''
                    alley = row[7] if len(row) > 7 else ''
                    
                    output_row = [areacode, '烏來區', road, lane, alley]
                    key = (road.strip(), lane.strip(), alley.strip())
                    if key not in seen:
                        seen.add(key)
                        rows.append(output_row)
        print(f'從原始資料重新生成，共 {len(rows)} 筆')
    else:
        print('找不到原始資料檔案')
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

# 依 路名、巷、弄 重新排序
print('\n正在排序資料...')
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'\n寫入檔案，共 {len(rows)} 筆資料...')
with open(file_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'完成！已更新烏來區門牌資料，共 {len(rows)} 筆')
print(f'檔案已儲存為：{file_path}')
print('資料已依路名/巷/弄排序')

# 驗證檔案
print('\n驗證檔案內容...')
with open(file_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f'標題: {header}')
    count = 0
    for row in reader:
        count += 1
        if count <= 5:
            print(f'第{count}行: {row}')
    print(f'總共 {count} 筆資料')
