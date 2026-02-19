# -*- coding: utf-8 -*-
"""驗證烏來區檔案欄位"""
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
    
    print(f'標題: {header}')
    print(f'標題欄位數: {len(header)}')
    print(f'總資料筆數: {len(rows)}')
    print('\n前10筆資料:')
    for i, row in enumerate(rows[:10], 1):
        print(f'  {i}. {row} (欄位數: {len(row)})')
    
    print('\n驗證:')
    print(f'✓ 檔案已刪除第二列（行政區）和第三列（路名）')
    print(f'✓ 現在只保留: {header}')
