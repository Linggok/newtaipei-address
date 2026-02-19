# -*- coding: utf-8 -*-
"""重新生成完整的烏來區門牌資料"""
import csv
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

# 可能的來源路徑
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_paths = [
    os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
]

# 烏來區代碼
WULAI_AREACODE = '65000290'

# 要添加的路名
new_roads = [
    ('大羅蘭', '', ''),
    ('天仁', '', ''),
    ('屯鹿', '', ''),
    ('卡拉模基', '', ''),
    ('李茂岸', '', ''),
    ('忠治', '', ''),
    ('金堰', '', ''),
    ('金堰', '１１５巷', ''),  # 金堰有115巷
    ('娃娃谷', '', ''),
    ('紅河', '', ''),
    ('馬岸', '', ''),
    ('桶後', '', ''),
    ('瀑布', '', ''),
]

# 找到來源檔案
input_path = None
for path in source_paths:
    if os.path.exists(path):
        input_path = path
        print(f'找到來源檔案: {input_path}')
        break

if not input_path:
    print('錯誤：找不到新北市門牌位置數值資料.csv')
    print('請確認檔案位於以下位置之一：')
    for path in source_paths:
        print(f'  - {path}')
    exit(1)

# 讀取並處理資料
seen = set()
rows = []

print('正在讀取原始資料...')
try:
    # 嘗試不同的編碼
    encodings = ['utf-8', 'utf-8-sig', 'cp950', 'big5']
    file_opened = False
    
    for encoding in encodings:
        try:
            with open(input_path, 'r', encoding=encoding) as infile:
                reader = csv.reader(infile)
                header = next(reader)
                print(f'成功讀取檔案，編碼: {encoding}')
                print(f'標題欄位: {header}')
                
                # 原始資料欄位：countycode(0), areacode(1), village(2), neighbor(3), 
                # street、road、section(4), area(5), lane(6), alley(7), number(8), ...
                for row in reader:
                    # 檢查第二欄（索引1）是否為烏來區代碼
                    if len(row) >= 2 and row[1] == WULAI_AREACODE:
                        # 提取欄位：areacode(1), 路名(4), 巷(6), 弄(7)
                        areacode = row[1] if len(row) > 1 else ''
                        road = row[4] if len(row) > 4 else ''
                        lane = row[6] if len(row) > 6 else ''
                        alley = row[7] if len(row) > 7 else ''
                        
                        # 建立輸出列：areacode, 行政區, 路名, 巷, 弄
                        output_row = [areacode, '烏來區', road, lane, alley]
                        
                        # 以 (路名, 巷, 弄) 去重
                        key = (road.strip(), lane.strip(), alley.strip())
                        if key not in seen:
                            seen.add(key)
                            rows.append(output_row)
                
                file_opened = True
                print(f'從原始資料讀取 {len(rows)} 筆不重複資料')
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f'使用編碼 {encoding} 時發生錯誤: {e}')
            continue
    
    if not file_opened:
        print('錯誤：無法讀取檔案，嘗試了多種編碼都失敗')
        exit(1)

except Exception as e:
    print(f'發生錯誤：{e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 添加新路名
print('\n添加新路名...')
added_count = 0
for road, lane, alley in new_roads:
    output_row = ['65000290', '烏來區', road, lane, alley]
    key = (road, lane, alley)
    if key not in seen:
        seen.add(key)
        rows.append(output_row)
        added_count += 1
        print(f'  ✓ 已添加: {road}, {lane}, {alley}')
    else:
        print(f'  - 已存在: {road}, {lane}, {alley}')

print(f'\n共添加 {added_count} 筆新路名')

# 依 路名、巷、弄 重新排序
print('\n正在排序資料...')
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'\n寫入檔案: {output_path}')
try:
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(output_header)
        writer.writerows(rows)
    
    print(f'✓ 完成！已重新生成烏來區門牌資料')
    print(f'  總筆數: {len(rows)} 筆')
    print(f'  格式: {output_header}')
    print(f'  檔案位置: {output_path}')
    
    # 顯示統計資訊
    roads = [row[2] for row in rows if row[2]]
    unique_roads = sorted(set(roads))
    print(f'\n統計資訊:')
    print(f'  不重複路名數: {len(unique_roads)}')
    print(f'  有巷的資料: {sum(1 for row in rows if row[3])} 筆')
    print(f'  有弄的資料: {sum(1 for row in rows if row[4])} 筆')
    
except PermissionError:
    print('錯誤：無法寫入檔案，檔案可能被其他程式開啟')
    print('請關閉 Cursor 或其他開啟此檔案的程式後再試')
    exit(1)
except Exception as e:
    print(f'寫入檔案時發生錯誤: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
