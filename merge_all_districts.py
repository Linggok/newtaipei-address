# -*- coding: utf-8 -*-
"""合併所有區的門牌資料到新北市門牌位置數值資料_with_area.csv，並刪除重複資料"""
import csv
import os
import sys

# 設定輸出編碼為 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(base_dir, '新北市門牌位置數值資料_with_area.csv')

# 所有區的 CSV 檔案列表（格式：檔案路徑, 行政區名稱）
district_files = [
    ('鶯歌區門牌位置數值資料.csv', '鶯歌區'),
    ('烏來區門牌位置數值資料.csv', '烏來區'),
    ('萬里區門牌位置數值資料.csv', '萬里區'),
    ('平溪區門牌位置數值資料.csv', '平溪區'),
    ('貢寮區門牌位置數值資料.csv', '貢寮區'),
    ('雙溪區門牌位置數值資料.csv', '雙溪區'),
    ('八里區門牌位置數值資料.csv', '八里區'),
    ('石門區門牌位置數值資料.csv', '石門區'),
    ('三芝區門牌位置數值資料.csv', '三芝區'),
    ('坪林區門牌位置數值資料.csv', '坪林區'),
    ('石碇區門牌位置數值資料.csv', '石碇區'),
    ('深坑區門牌位置數值資料.csv', '深坑區'),
    ('泰山區門牌位置數值資料.csv', '泰山區'),
    ('林口區門牌位置數值資料.csv', '林口區'),
    ('五股區門牌位置數值資料.csv', '五股區'),
    ('蘆洲區門牌位置數值資料.csv', '蘆洲區'),
    ('土城區門牌位置數值資料.csv', '土城區'),
    ('瑞芳區門牌位置數值資料.csv', '瑞芳區'),
    ('新店區門牌位置數值資料.csv', '新店區'),
    ('汐止區門牌位置數值資料.csv', '汐止區'),
    ('淡水區門牌位置數值資料.csv', '淡水區'),
    ('三峽區門牌位置數值資料.csv', '三峽區'),
    ('樹林區門牌位置數值資料.csv', '樹林區'),
    ('永和區門牌位置數值資料.csv', '永和區'),
]

all_rows = []
seen = set()

print('開始合併各區門牌資料...')

for filename, district_name in district_files:
    file_path = os.path.join(base_dir, filename)
    if not os.path.exists(file_path):
        print(f'警告：找不到檔案 {filename}，跳過')
        continue
    
    print(f'讀取 {filename}...')
    try:
        # 嘗試不同的編碼
        encodings = ['utf-8-sig', 'utf-8', 'cp950', 'big5']
        file_opened = False
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as infile:
                    reader = csv.reader(infile)
                    header = next(reader)
                    
                    # 檢查欄位順序：areacode, 行政區, 路名, 巷, 弄
                    if len(header) < 5:
                        print(f'  警告：{filename} 欄位不足，跳過')
                        break
                    
                    count = 0
                    for row in reader:
                        if len(row) < 5:
                            continue
                        
                        # 提取欄位
                        areacode = row[0].strip() if len(row) > 0 else ''
                        district = row[1].strip() if len(row) > 1 else district_name
                        road = row[2].strip() if len(row) > 2 else ''
                        lane = row[3].strip() if len(row) > 3 else ''
                        alley = row[4].strip() if len(row) > 4 else ''
                        
                        # 建立輸出列：areacode, 行政區, 路名, 巷, 弄
                        output_row = [areacode, district, road, lane, alley]
                        
                        # 以 (行政區, 路名, 巷, 弄) 去重
                        key = (district, road, lane, alley)
                        if key not in seen:
                            seen.add(key)
                            all_rows.append(output_row)
                            count += 1
                    
                    print(f'  已讀取 {count} 筆資料')
                    file_opened = True
                    break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f'  使用編碼 {encoding} 時發生錯誤: {e}')
                continue
        
        if not file_opened:
            print(f'  錯誤：無法讀取 {filename}')
    except Exception as e:
        print(f'讀取 {filename} 時發生錯誤: {e}')
        import traceback
        traceback.print_exc()

# 依 行政區、路名、巷、弄 重新排序
print('正在排序資料...')
all_rows.sort(key=lambda r: (r[1], r[2], r[3], r[4]))

# 輸出標題：areacode,行政區,路名,巷,弄
output_header = ['areacode', '行政區', '路名', '巷', '弄']

print(f'寫入合併後的檔案，共 {len(all_rows)} 筆資料...')
with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(output_header)
    writer.writerows(all_rows)

print(f'完成！已合併 {len(district_files)} 個區的資料，共 {len(all_rows)} 筆不重複門牌資料')
print(f'檔案已儲存為：{output_path}')
print('資料已依行政區/路名/巷/弄排序')
