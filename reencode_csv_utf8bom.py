# -*- coding: utf-8 -*-
"""將 CSV 以 UTF-8（含 BOM）重新寫入，避免開啟/編輯後亂碼"""
import os
import sys

def reencode_to_utf8_bom(filepath):
    """嘗試用 UTF-8 或 Big5 讀取，再以 UTF-8 BOM 寫回"""
    for enc in ('utf-8', 'utf-8-sig', 'cp950', 'big5'):
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    else:
        print('Read failed')
        return False
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(content)
    print('OK')
    return True

if __name__ == '__main__':
    path = r'c:\Users\user\Desktop\newtaipei\鶯歌區門牌位置數值資料.csv'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    if not os.path.isfile(path):
        print('File not found')
        sys.exit(1)
    reencode_to_utf8_bom(path)
