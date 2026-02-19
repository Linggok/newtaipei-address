# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選新店區資料，填入行政區欄位，同時去重並重新排列"""
import csv

input_path = r'c:\Users\user\Desktop\新北市\新北市門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\新店區門牌位置數值資料.csv'

# 新店區代碼
XINDIAN_AREACODE = '65000060'

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
        if len(row) > 1 and row[1] == XINDIAN_AREACODE:
            # 在 areacode 之後插入「新店區」
            new_row = row[:areacode_idx+1] + ['新店區'] + row[areacode_idx+1:]
            # 去重：以完整列為 key
            key = tuple(new_row)
            if key not in seen:
                seen.add(key)
                rows.append(new_row)

# 重新排列：依 路名、巷、弄 排序
def sort_key(r):
    # street、road、section 欄位索引（在插入行政區後）
    road_idx = new_header.index('street、road、section')
    lane_idx = new_header.index('lane')
    alley_idx = new_header.index('alley')
    road = (r[road_idx] if len(r) > road_idx else '').strip()
    lane = (r[lane_idx] if len(r) > lane_idx else '').strip()
    alley = (r[alley_idx] if len(r) > alley_idx else '').strip()
    return (road, lane, alley)

rows.sort(key=sort_key)

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)
    writer.writerows(rows)

print('Done:', len(rows), 'unique rows saved')
