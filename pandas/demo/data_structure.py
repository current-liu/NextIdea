#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 9:21 AM

base Info
"""
#"http://www.cnblogs.com/nxld/p/6058591.html"
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

"""Series"""
arr1 = np.arange(10)
t1 = type(arr1)
print t1
s1 = pd.Series(arr1)
# type(s1)


dic1 = {'a': 1, 'b': 2, 'c': 3}
s2 = pd.Series(dic1)
type(s2)

"""DataFrame"""

arr2 = np.array(np.arange(12).reshape(4, 3))
df1 = pd.DataFrame(arr2)

dic2 = {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8], 'c': [9, 10, 11, 12]}
df2 = pd.DataFrame(dic2)

dic3 = {'one': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 'two': {'a': 5, 'b': 6, 'c': 7, 'd': 8},
        'three': {'a': 9, 'b': 10, 'c': 11, 'd': 12}}
df3 = pd.DataFrame(dic3)

df4 = df3[['one', 'three']]
s3 = df3['one']

pass
