# -*- coding: utf-8 -*-
"""從 鶯歌區門牌位置數值資料.csv 移除重複列，覆寫原檔"""
import csv
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '鶯歌區門牌位置數值資料.csv')
if not os.path.isfile(path):
    print('File not found:', path)
    exit(1)

seen = set()
rows = []

with open(path, 'r', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows.append(header)
    
    for row in reader:
        if not row or not any(row):  # 跳過空行
            continue
        # 以完整列為 key 去重
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            rows.append(row)

before_count = sum(1 for line in open(path, 'r', encoding='utf-8-sig')) - 1  # 減去表頭
after_count = len(rows) - 1  # 減去表頭

with open(path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f'已刪除 {before_count - after_count} 筆重複資料。')
print(f'原本 {before_count} 筆 → 現在 {after_count} 筆（唯一）')
