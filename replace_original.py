# -*- coding: utf-8 -*-
import os
import shutil

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
folder = os.path.join(desktop, '\u65b0\u5317\u5e02')
filtered = os.path.join(folder, '\u65b0\u5317\u5e02\u9580\u724c\u4f4d\u7f6e\u6578\u503c\u8cc7\u6599_filtered.csv')
original = os.path.join(folder, '\u65b0\u5317\u5e02\u9580\u724c\u4f4d\u7f6e\u6578\u503c\u8cc7\u6599.csv')
if os.path.exists(filtered):
    shutil.move(filtered, original)
    print('OK: original file replaced with filtered data')
else:
    print('Filtered file not found')
