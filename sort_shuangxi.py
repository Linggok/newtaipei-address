# -*- coding: utf-8 -*-
import csv
path = r'c:\Users\user\Desktop\newtaipei\雙溪區門牌位置數值資料.csv'
with open(path, 'r', encoding='utf-8-sig') as f:
    r = csv.reader(f)
    header = next(r)
    rows = list(r)
rows.sort(key=lambda x: (x[2] if len(x) > 2 else '', x[3] if len(x) > 3 else '', x[4] if len(x) > 4 else ''))
with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)
print('已依路名、巷、弄排序，共', len(rows), '筆')
