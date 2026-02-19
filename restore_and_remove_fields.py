# -*- coding: utf-8 -*-
"""復原烏來區檔案並刪除第二欄和第三欄"""
import csv
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
temp_file = os.path.join(base_dir, '烏來區門牌位置數值資料_temp.csv')
output_file = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

# 先讀取臨時檔案（如果存在）
if os.path.exists(temp_file):
    print(f'讀取臨時檔案: {temp_file}')
    with open(temp_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        print(f'從臨時檔案讀取 {len(rows)} 筆資料')
else:
    # 如果沒有臨時檔案，從原始資料生成
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    source_path = os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv')
    
    if not os.path.exists(source_path):
        print('錯誤：找不到原始資料檔案')
        exit(1)
    
    print(f'從原始資料讀取: {source_path}')
    rows = []
    seen = set()
    
    with open(source_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if len(row) >= 2 and row[1] == '65000290':
                areacode = row[1]
                road = row[4] if len(row) > 4 else ''
                lane = row[6] if len(row) > 6 else ''
                alley = row[7] if len(row) > 7 else ''
                
                output_row = [areacode, '烏來區', road, lane, alley]
                key = (road.strip(), lane.strip(), alley.strip())
                if key not in seen:
                    seen.add(key)
                    rows.append(output_row)
    
    # 添加新路名
    new_roads = [
        ('大羅蘭', '', ''), ('天仁', '', ''), ('屯鹿', '', ''),
        ('卡拉模基', '', ''), ('李茂岸', '', ''), ('忠治', '', ''),
        ('金堰', '', ''), ('金堰', '１１５巷', ''),
        ('娃娃谷', '', ''), ('紅河', '', ''), ('馬岸', '', ''),
        ('桶後', '', ''), ('瀑布', '', ''),
    ]
    
    for road, lane, alley in new_roads:
        output_row = ['65000290', '烏來區', road, lane, alley]
        key = (road, lane, alley)
        if key not in seen:
            seen.add(key)
            rows.append(output_row)
    
    rows.sort(key=lambda r: (r[2], r[3], r[4]))
    print(f'從原始資料生成 {len(rows)} 筆資料')

# 刪除第二欄（行政區）和第三欄（路名）
print('\n刪除第二欄（行政區）和第三欄（路名）...')
new_header = ['areacode', '巷', '弄']
new_rows = []
for row in rows:
    if len(row) >= 5:
        new_row = [row[0], row[3], row[4]]
        new_rows.append(new_row)

print(f'處理後剩餘 {len(new_rows)} 筆資料')

# 寫入檔案
print(f'\n寫入檔案: {output_file}')
try:
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        writer.writerows(new_rows)
    print(f'完成！檔案已更新')
    print(f'格式: {new_header}')
    print(f'共 {len(new_rows)} 筆資料')
    
    # 刪除臨時檔案
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print('已刪除臨時檔案')
        
except PermissionError:
    print('錯誤：無法寫入檔案，檔案可能被其他程式開啟')
    print('請關閉 Cursor 或其他開啟此檔案的程式後再試')
