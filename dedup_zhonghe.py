# -*- coding: utf-8 -*-
"""從 zhonghe_real_data.csv 移除重複列，覆寫原檔"""
import pandas as pd
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zhonghe_real_data.csv')
if not os.path.isfile(path):
    print('File not found:', path)
    exit(1)

df = pd.read_csv(path, encoding='utf-8-sig')
before = len(df)
df = df.drop_duplicates()
df.to_csv(path, index=False, encoding='utf-8-sig')
print('Removed', before - len(df), 'duplicates. Now', len(df), 'unique rows.')
