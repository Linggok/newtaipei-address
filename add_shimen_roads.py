# -*- coding: utf-8 -*-
"""在石門區門牌資料中新增指定路名（巷、弄留空），去重後依路名/巷/弄排序"""
import csv

CSV_PATH = r'c:\Users\user\Desktop\newtaipei\石門區門牌位置數值資料.csv'
AREACODE = '65000220'
DISTRICT = '石門區'

# 要新增的路名（僅路名，巷弄留空）
NEW_ROADS = [
    '七股', '九芎林', '八甲', '下員坑', '大丘田', '大溪墘', '小坑', '五爪崙',
    '內石門', '內阿里磅', '公地', '白沙灣別墅', '石門新村', '石崩山', '尖子鹿',
    '尖山湖', '竹子湖', '老崩山', '坪林', '金華新城', '阿里荖', '阿里磅',
    '茂林社區', '崁子腳', '海灣新城', '草埔尾', '楓林', '楓林23之2', '臨海別墅', '豬糟潭',
]

def main():
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 以 (路名, 巷, 弄) 為 key 去重（保留既有列）
    seen = set()
    out = []
    for row in rows:
        if len(row) < 5:
            row = row + ['', '', '']  # 補足 5 欄
        ac, area, road, lane, alley = (row[0], row[1], row[2].strip(), row[3].strip(), row[4].strip())
        key = (road, lane, alley)
        if key not in seen:
            seen.add(key)
            out.append([ac, area, road, lane, alley])

    # 加入新路名（巷、弄留空）
    for road in NEW_ROADS:
        road = road.strip()
        if not road:
            continue
        key = (road, '', '')
        if key not in seen:
            seen.add(key)
            out.append([AREACODE, DISTRICT, road, '', ''])

    # 依 路名、巷、弄 排序
    out.sort(key=lambda r: (r[2], r[3], r[4]))

    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(out)

    print('OK', len(out), 'rows')

if __name__ == '__main__':
    main()
