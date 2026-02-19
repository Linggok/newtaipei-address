# -*- coding: utf-8 -*-
"""檢查金堰115巷資料"""
import csv
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

with open(file_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
    
    print('所有金堰相關資料:')
    for row in rows:
        if row[2] == '金堰':
            print(f'  {row}')
    
    print('\n檢查115巷:')
    for row in rows:
        if row[2] == '金堰':
            lane = row[3]
            print(f'  路名: {row[2]}, 巷: [{lane}], 長度: {len(lane)}, 包含115: {"115" in lane}')
