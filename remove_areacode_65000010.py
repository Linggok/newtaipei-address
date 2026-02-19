# -*- coding: utf-8 -*-
"""
從「新北市門牌位置數值資料」CSV 中刪除代碼 65000010（板橋區）的資料列。
會先備份原檔，再覆寫原檔。
"""
import pandas as pd
import os
import shutil
import sys
from datetime import datetime

# Windows 主控台 UTF-8 輸出
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

# 可能的來源路徑（與 filter_yonghe.py 一致）
source_paths = [
    os.path.join(desktop, '新北市', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '板橋', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '板橋區', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, 'newtaipei', '新北市門牌位置數值資料.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料1.csv'),
    os.path.join(desktop, '新北市門牌位置數值資料.csv'),
]

TARGET_AREACODE = '65000010'  # 板橋區，要刪除的代碼


def main():
    source_file = None
    for p in source_paths:
        if os.path.isfile(p):
            source_file = p
            break

    if not source_file:
        print('CSV not found. Check one of these paths:')
        for p in source_paths:
            print('  -', p)
        return

    try:
        print('Reading:', source_file)
        try:
            df = pd.read_csv(source_file, encoding='utf-8', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(source_file, encoding='cp950', low_memory=False)

        # 找出代碼欄位（areacode 或 代碼）
        code_col = None
        if 'areacode' in df.columns:
            code_col = 'areacode'
        elif '代碼' in df.columns:
            code_col = '代碼'
        else:
            print('Error: no areacode/代碼 column. Columns:', list(df.columns))
            return

        before = len(df)
        # 刪除代碼為 65000010 的列
        df = df[df[code_col].astype(str).str.strip() != TARGET_AREACODE].copy()
        removed = before - len(df)

        if removed == 0:
            print(f'No rows with areacode {TARGET_AREACODE} found. No change.')
            return

        # 備份原檔
        backup_path = source_file + '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.copy2(source_file, backup_path)
        print('Backup saved:', backup_path)

        # 寫回原檔
        try:
            df.to_csv(source_file, index=False, encoding='utf-8-sig')
        except Exception:
            df.to_csv(source_file, index=False, encoding='cp950')
        print(f'Removed {removed} rows with areacode {TARGET_AREACODE}. Saved to: {source_file}')
        print(f'Remaining rows: {len(df)}')

    except Exception as e:
        print('Error:', e)
        raise


if __name__ == '__main__':
    main()
