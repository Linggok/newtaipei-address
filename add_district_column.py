# -*- coding: utf-8 -*-
"""為 banqiao_real_data.csv 在路名前新增「行政區」欄位"""
import pandas as pd
import os

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, 'banqiao_real_data.csv')
out = os.path.join(base, 'banqiao_real_data.csv')

df = pd.read_csv(path, encoding='utf-8', low_memory=False)
if '行政區' not in df.columns:
    df.insert(2, '行政區', '板橋區')
df.to_csv(out, index=False, encoding='utf-8-sig')
print('已新增「行政區」欄位，並儲存為', out)
