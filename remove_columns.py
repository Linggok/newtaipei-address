# -*- coding: utf-8 -*-
"""刪除CSV檔案的第二列和第三列（行政區和路名）"""
import csv
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')
output_file = os.path.join(base_dir, '烏來區門牌位置數值資料.csv')

print(f'讀取檔案: {input_file}')

rows = []
try:
    with open(input_file, 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        print(f'原始標題: {header}')
        
        # 刪除第二列（索引1，行政區）和第三列（索引2，路名）
        # 保留：areacode(0), 巷(3), 弄(4)
        # 清理 BOM 標記
        areacode_col = header[0].replace('\ufeff', '').strip()
        if not areacode_col:
            areacode_col = 'areacode'
        
        # 檢查標題欄位數量
        if len(header) >= 5:
            new_header = [areacode_col, header[3], header[4]]
            print(f'新標題: {new_header}')
            
            for row in reader:
                if len(row) >= 5:
                    # 只保留第1列（areacode）、第4列（巷）、第5列（弄）
                    new_row = [row[0], row[3], row[4]]
                    rows.append(new_row)
        else:
            # 如果已經只有3列，檢查是否需要處理
            print(f'檔案已經只有 {len(header)} 列，標題: {header}')
            if len(header) == 3:
                print('檔案已經是3列格式，無需修改')
                exit(0)
            else:
                # 如果格式不同，嘗試處理
                new_header = [areacode_col]
                if len(header) > 3:
                    new_header.append(header[3] if len(header) > 3 else '巷')
                if len(header) > 4:
                    new_header.append(header[4] if len(header) > 4 else '弄')
                print(f'新標題: {new_header}')
                
                for row in reader:
                    if len(row) >= len(header):
                        new_row = [row[0]]
                        if len(row) > 3:
                            new_row.append(row[3])
                        if len(row) > 4:
                            new_row.append(row[4])
                        rows.append(new_row)
        
        print(f'已處理 {len(rows)} 筆資料')
        
except Exception as e:
    print(f'讀取檔案時發生錯誤: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 寫入新檔案
print(f'\n寫入檔案: {output_file}')
with open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)
    writer.writerows(rows)

print(f'完成！已刪除第二列和第三列')
print(f'檔案已更新，共 {len(rows)} 筆資料')
print(f'新格式: {new_header}')

# 顯示前5筆資料作為確認
print('\n前5筆資料:')
for i, row in enumerate(rows[:5], 1):
    print(f'  {i}. {row}')
