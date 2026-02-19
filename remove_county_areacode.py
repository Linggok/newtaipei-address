# -*- coding: utf-8 -*-
"""從 banqiao_real_data.csv 刪除 countycode、areacode 兩欄"""
import pandas as pd
import os

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, 'banqiao_real_data.csv')

df = pd.read_csv(path, encoding='utf-8', low_memory=False)
df = df.drop(columns=['countycode', 'areacode'], errors='ignore')
df.to_csv(path, index=False, encoding='utf-8-sig')
print('已刪除 countycode、areacode 兩欄。')
