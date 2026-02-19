# -*- coding: utf-8 -*-
"""從新北市門牌位置數值資料中篩選烏來區資料（代號65000290），填入行政區、去重並重新排序"""
import csv
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 可能的來源路徑
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
source_paths = [
    os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
]

# 烏來區代碼
WULAI_AREACODE = '65000290'

# 輸出路徑
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '烏來區門牌位置數值資料.csv')

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
                # 以 (路名, 巷, 弄) 去重，保留一筆
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

# 依 路名、巷、弄 重新排序
rows.sort(key=lambda r: (r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(rows)

print(f'完成：已篩選出 {len(rows)} 筆不重複的烏來區門牌資料')
print(f'檔案已儲存為：{output_path}')
print('資料已依路名/巷/弄排序')
