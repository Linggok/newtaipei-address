# -*- coding: utf-8 -*-
"""
轉換大同區檔案編碼
使用 Python 的 chardet 自動偵測編碼
"""

import sys
import os

try:
    import chardet
except ImportError:
    print("請安裝 chardet: pip install chardet")
    sys.exit(1)

input_file = os.path.join(os.path.dirname(__file__), '大同區門牌位置數值資料.CSV')
output_file = os.path.join(os.path.dirname(__file__), '大同區門牌位置數值資料_utf8.CSV')

print(f"讀取檔案: {input_file}")

# 讀取檔案並偵測編碼
with open(input_file, 'rb') as f:
    raw_data = f.read()

# 偵測編碼
detected = chardet.detect(raw_data)
print(f"偵測到的編碼: {detected['encoding']}, 信心度: {detected['confidence']}")

# 嘗試解碼
encodings_to_try = [
    detected['encoding'] if detected['encoding'] else None,
    'utf-8',
    'big5',
    'cp950',
    'gb2312',
    'gbk',
    'gb18030',
    'utf-8-sig'  # UTF-8 with BOM
]

content = None
used_encoding = None

for encoding in encodings_to_try:
    if not encoding:
        continue
    try:
        if encoding == 'utf-8-sig':
            content = raw_data.decode('utf-8-sig')
        else:
            content = raw_data.decode(encoding)
        
        # 檢查是否包含正確的中文字
        if '區名' in content or '街路段' in content or '大同區' in content:
            used_encoding = encoding
            print(f"✓ 成功使用編碼: {encoding}")
            break
    except Exception as e:
        continue

if not content:
    print("無法解碼檔案")
    sys.exit(1)

# 儲存為 UTF-8
with open(output_file, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print(f"✓ 已轉換為 UTF-8 並儲存為: {output_file}")
print(f"使用編碼: {used_encoding}")
print(f"\n前 500 字符:")
print(content[:500])
