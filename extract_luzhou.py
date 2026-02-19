# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選蘆洲區資料（代號65000140），填入行政區、去重並重新排序"""
import csv

input_path = r'c:\Users\user\Desktop\新北市\新北市門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\蘆洲區門牌位置數值資料.csv'

# 蘆洲區代碼
LUZHOU_AREACODE = '65000140'

with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    # 以 (路名, 巷, 弄) 去重，保留一筆
    seen = set()
    rows = []
    for row in reader:
        if len(row) >= 2 and row[1] == LUZHOU_AREACODE:
            areacode = row[1] if len(row) > 1 else ''
            road = row[4] if len(row) > 4 else ''
            lane = row[6] if len(row) > 6 else ''
            alley = row[7] if len(row) > 7 else ''
            output_row = [areacode, '蘆洲區', road, lane, alley]
            key = (road.strip(), lane.strip(), alley.strip())
            if key not in seen:
                seen.add(key)
                rows.append(output_row)

# 依 路名、巷、弄 重新排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

output_header = ['areacode', '行政區', '路名', '巷', '弄']
with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print('Done:', len(rows), 'rows written to Luzhou CSV, sorted by road/lane/alley')
