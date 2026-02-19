# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料篩選永和區(65000040)"""
import csv
import os

src = os.path.join(os.path.expanduser("~"), "Desktop", "新北市", "新北市門牌位置數值資料.csv")
dst = os.path.join(os.path.expanduser("~"), "Desktop", "newtaipei", "永和區門牌位置數值資料.csv")
YONGHE_CODE = "65000040"

with open(src, "r", encoding="utf-8") as fin:
    reader = csv.reader(fin)
    header = next(reader)
    with open(dst, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(header)
        count = 0
        for row in reader:
            if len(row) >= 2 and row[1] == YONGHE_CODE:
                writer.writerow(row)
                count += 1
print(f"Done: {count} rows -> {dst}")
