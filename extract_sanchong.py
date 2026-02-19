# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選三重區資料，並填入行政區欄位，同時去重"""
import csv

input_path = r'c:\Users\user\Desktop\新北市\新北市門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\三重區門牌位置數值資料.csv'

# 三重區代碼
SANCHONG_AREACODE = '65000020'

with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    
    # 在 areacode 之後插入「行政區」欄位
    # 原始欄位：countycode,areacode,village,neighbor,street、road、section,area,lane,alley,number,x_3826,y_3826
    # 新欄位：countycode,areacode,行政區,village,neighbor,street、road、section,area,lane,alley,number,x_3826,y_3826
    areacode_idx = header.index('areacode')
    new_header = header[:areacode_idx+1] + ['行政區'] + header[areacode_idx+1:]
    
    seen = set()
    rows = []
    for row in reader:
        # areacode 在第2欄（索引1）
        if len(row) > 1 and row[1] == SANCHONG_AREACODE:
            # 在 areacode 之後插入「三重區」
            new_row = row[:areacode_idx+1] + ['三重區'] + row[areacode_idx+1:]
            key = tuple(new_row)
            if key not in seen:
                seen.add(key)
                rows.append(new_row)

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)
    writer.writerows(rows)

print(f'Done: {len(rows)} unique rows saved')
