#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 9:58 AM

base Info
"""
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

s4 = pd.Series(np.array([1, 1, 2, 3, 5, 8]))
print s4
print s4.index
s4.index = ['a', 'b', 'c', 'd', 'e', 'f']

print s4[3]
print s4['e']
print s4[[1, 3, 5]]
print s4[['a', 'b', 'd', 'f']]
print s4[:4]
print s4['c':]
print s4['b':'e']

s5 = pd.Series(np.array([10, 15, 20, 30, 55, 80]),
               index=['a', 'b', 'c', 'd', 'e', 'f'])
print s5
s6 = pd.Series(np.array([12, 11, 13, 15, 14, 16]),
               index=['a', 'c', 'g', 'b', 'd', 'f'])
print s6
print s5 + s6
print s5 / s6
