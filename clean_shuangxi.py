# -*- coding: utf-8 -*-
"""清理雙溪區門牌資料，去除重複並重新排列"""
import csv

input_path = r'c:\Users\user\Desktop\newtaipei\雙溪區門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\雙溪區門牌位置數值資料.csv'

seen = set()
rows = []

with open(input_path, 'r', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    
    for row in reader:
        if len(row) < 5:
            continue
        
        areacode = row[0].strip() if len(row) > 0 else ''
        district = row[1].strip() if len(row) > 1 else ''
        road = row[2].strip() if len(row) > 2 else ''
        lane = row[3].strip() if len(row) > 3 else ''
        alley = row[4].strip() if len(row) > 4 else ''
        
        # 統一「自強路」和「自强路」為「自強路」（繁體）
        if road == '自强路':
            road = '自強路'
        
        # 建立去重的 key
        key = (road, lane, alley)
        
        if key not in seen:
            seen.add(key)
            rows.append([areacode, district, road, lane, alley])

# 依 路名、巷、弄 重新排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出
output_header = ['areacode', '行政區', '路名', '巷', '弄']

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'Done: {len(rows)} 筆不重複門牌已寫入，並已依路名/巷/弄排序')
