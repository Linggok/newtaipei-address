# -*- coding: utf-8 -*-
"""驗證烏來區檔案內容"""
import csv
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

new_roads = ['大羅蘭', '天仁', '屯鹿', '卡拉模基', '李茂岸', '忠治', '金堰', '娃娃谷', '紅河', '馬岸', '桶後', '瀑布']

with open(file_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f'標題: {header}\n')
    
    rows = list(reader)
    roads = [row[2] for row in rows if row[2]]
    unique_roads = sorted(set(roads))
    
    print(f'總資料筆數: {len(rows)}')
    print(f'不重複路名數: {len(unique_roads)}\n')
    
    print('檢查新路名:')
    for road in new_roads:
        found = road in roads
        print(f'  {road}: {"✓" if found else "✗"}')
    
    print('\n檢查金堰115巷:')
    jin_yan_115 = [row for row in rows if row[2] == '金堰' and ('115' in row[3] or '１１５' in row[3])]
    print(f'  找到 {len(jin_yan_115)} 筆金堰115巷資料')
    for row in jin_yan_115:
        print(f'    {row}')
    
    print('\n所有路名列表:')
    for i, road in enumerate(unique_roads, 1):
        print(f'  {i}. {road}')
