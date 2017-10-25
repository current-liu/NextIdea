#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 10:35 AM

base Info
"""
import numpy as np, pandas as pd
__author__ = 'liuchao'
__version__ = '1.0'

visitor = pd.io.parsers.read_csv('./sale_order_visitors.csv')
print visitor.head()
a = visitor.ix[[0,1,2]]
b = visitor[['id','order_id','ip','location']].head()
c = visitor.ix[:,['id','order_id','ip','location']]
d = visitor.ix[[0,1,2],['id','order_id','ip','location']]

e = visitor[visitor['location']=="China Shaanxi Xi'an"]
f = visitor[(visitor['location']=="China Shaanxi Xi'an") | (visitor['location']=="Australia Victoria Melbourne")]
pass





