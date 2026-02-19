# -*- coding: utf-8 -*-
"""驗證重新生成的泰山區檔案"""
import csv
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '泰山區門牌位置數值資料.csv')

with open(file_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
    
    print(f'標題: {header}')
    print(f'標題欄位數: {len(header)}')
    print(f'總資料筆數: {len(rows)}\n')
    
    # 統計資訊
    roads = [row[2] for row in rows if row[2]]
    unique_roads = sorted(set(roads))
    
    print(f'統計資訊:')
    print(f'  不重複路名數: {len(unique_roads)}')
    print(f'  有巷的資料: {sum(1 for row in rows if row[3])} 筆')
    print(f'  有弄的資料: {sum(1 for row in rows if row[4])} 筆')
    
    print(f'\n前10筆資料範例:')
    for i, row in enumerate(rows[:10], 1):
        print(f'  {i:2d}. {row}')
    
    print(f'\n前10個路名:')
    for i, road in enumerate(unique_roads[:10], 1):
        count = sum(1 for row in rows if row[2] == road)
        print(f'  {i:2d}. {road} ({count} 筆)')
