# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選樹林區資料，並填入行政區欄位、去重、重新排列"""
import csv

input_path = r'c:\Users\user\Desktop\新北市\新北市門牌位置數值資料.csv'
output_path = r'c:\Users\user\Desktop\newtaipei\樹林區門牌位置數值資料.csv'

# 樹林區代碼
SHULIN_AREACODE = '65000070'

with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    
    # 找到欄位索引
    # 原始格式：countycode,areacode,village,neighbor,street、road、section,area,lane,alley,number,x_3826,y_3826
    idx_areacode = header.index('areacode') if 'areacode' in header else 1
    idx_road = header.index('street、road、section') if 'street、road、section' in header else 4
    idx_lane = header.index('lane') if 'lane' in header else 6
    idx_alley = header.index('alley') if 'alley' in header else 7
    
    # 以 (路名, 巷, 弄) 為 key 去重，保留第一次出現的整列
    seen = set()
    rows = []
    for row in reader:
        if len(row) > idx_areacode and row[idx_areacode] == SHULIN_AREACODE:
            road = row[idx_road] if len(row) > idx_road else ''
            lane = row[idx_lane] if len(row) > idx_lane else ''
            alley = row[idx_alley] if len(row) > idx_alley else ''
            
            # 跳過路名為空的資料
            if not road.strip():
                continue
                
            # 路名、巷、弄 為去重 key（相同門牌只保留一筆）
            key = (road.strip(), lane.strip(), alley.strip())
            if key not in seen:
                seen.add(key)
                # 輸出格式：areacode,行政區,路名,巷,弄
                output_row = [
                    SHULIN_AREACODE,
                    '樹林區',
                    road.strip(),
                    lane.strip(),
                    alley.strip()
                ]
                rows.append(output_row)

    # 重新排列：依 路名、巷、弄 排序
    rows.sort(key=lambda r: (
        r[2] if len(r) > 2 else '',  # 路名
        r[3] if len(r) > 3 else '',  # 巷
        r[4] if len(r) > 4 else '',  # 弄
    ))

# 寫入輸出檔案
output_header = ['areacode', '行政區', '路名', '巷', '弄']
with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print('Done: {} unique rows saved'.format(len(rows)))
