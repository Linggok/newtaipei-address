# -*- coding: utf-8 -*-
"""移除新北市門牌資料中指定 areacode 的資料列"""
import csv
import os

REMOVE_CODES = {'65000020', '65000030', '65000040', '65000050'}
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
# 新北市資料夾（與桌面上顯示的名稱一致）
folder = os.path.join(desktop, '\u65b0\u5317\u5e02')  # 新北市
input_path = os.path.join(folder, '\u65b0\u5317\u5e02\u9580\u724c\u4f4d\u7f6e\u6578\u503c\u8cc7\u6599.csv')
output_path = os.path.join(folder, '\u65b0\u5317\u5e02\u9580\u724c\u4f4d\u7f6e\u6578\u503c\u8cc7\u6599_filtered.csv')

removed = 0
kept = 0

with open(input_path, 'r', encoding='utf-8') as inf:
    with open(output_path, 'w', encoding='utf-8', newline='') as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if not row:
                continue
            areacode = row[0].strip() if row else ''
            if areacode in REMOVE_CODES:
                removed += 1
            else:
                writer.writerow(row)
                kept += 1

print('Removed (65000020,65000030,65000040,65000050):', removed)
print('Kept:', kept)
print('Output:', output_path)
