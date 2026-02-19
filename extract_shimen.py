# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選石門區資料（代號65000220），填入行政區、去重並重新排序"""
import csv

input_path = r'c:\Users\user\Desktop\新北市\新北市門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\石門區門牌位置數值資料.csv'

# 石門區代碼
SHIMEN_AREACODE = '65000220'

with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    # 原始資料欄位：countycode(0), areacode(1), village(2), neighbor(3),
    # street、road、section(4), area(5), lane(6), alley(7), number(8), ...
    # 以 (路名, 巷, 弄) 去重，保留一筆
    seen = set()
    rows = []
    for row in reader:
        # 檢查第二欄（索引1）是否為石門區代碼
        if len(row) >= 2 and row[1] == SHIMEN_AREACODE:
            # 提取欄位：areacode(1), 路名(4), 巷(6), 弄(7)
            areacode = row[1] if len(row) > 1 else ''
            road = row[4] if len(row) > 4 else ''
            lane = row[6] if len(row) > 6 else ''
            alley = row[7] if len(row) > 7 else ''

            # 建立輸出列：areacode, 行政區, 路名, 巷, 弄
            output_row = [areacode, '石門區', road, lane, alley]

            # 以 (路名, 巷, 弄) 去重
            key = (road.strip(), lane.strip(), alley.strip())
            if key not in seen:
                seen.add(key)
                rows.append(output_row)

# 依 路名、巷、弄 重新排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'Done: {len(rows)} 筆不重複門牌已寫入，並已依路名/巷/弄排序')
