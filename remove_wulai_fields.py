# -*- coding: utf-8 -*-
"""刪除烏來區資料的第二欄（行政區）和第三欄（路名）"""
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
        
        # 刪除第二欄（索引1，行政區）和第三欄（索引2，路名）
        # 保留：areacode(0), 巷(3), 弄(4)
        # 清理 BOM 標記
        areacode_col = header[0].replace('\ufeff', '').strip()
        if not areacode_col:
            areacode_col = 'areacode'
        
        if len(header) >= 5:
            new_header = [areacode_col, header[3], header[4]]
            print(f'新標題: {new_header}')
            
            for row in reader:
                if len(row) >= 5:
                    # 只保留第1欄（areacode）、第4欄（巷）、第5欄（弄）
                    new_row = [row[0], row[3], row[4]]
                    rows.append(new_row)
        else:
            print(f'錯誤：檔案欄位數不足，只有 {len(header)} 欄')
            print(f'當前標題: {header}')
            exit(1)
        
        print(f'已處理 {len(rows)} 筆資料')
        
except Exception as e:
    print(f'讀取檔案時發生錯誤: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 寫入檔案
print(f'\n寫入檔案: {output_file}')
try:
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(new_header)
        writer.writerows(rows)
    
    print(f'✓ 完成！已刪除第二欄（行政區）和第三欄（路名）')
    print(f'  檔案已更新，共 {len(rows)} 筆資料')
    print(f'  新格式: {new_header}')
    
    # 顯示前5筆資料作為確認
    print('\n前5筆資料:')
    for i, row in enumerate(rows[:5], 1):
        print(f'  {i}. {row}')
        
except PermissionError:
    print('錯誤：無法寫入檔案，檔案可能被其他程式開啟')
    print('請關閉 Cursor 或其他開啟此檔案的程式後再試')
    exit(1)
except Exception as e:
    print(f'寫入檔案時發生錯誤: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
