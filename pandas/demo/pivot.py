#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 4:35 PM

base Info
"""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

__author__ = 'liuchao'
__version__ = '1.0'

# pivot_table(data, values=None,
#             index=None,
#             columns=None,
#             aggfunc='mean',
#             fill_value=None,
#             margins=False,
#             dropna=True,
#             margins_name='All')

# data：需要进行数据透视表操作的数据框
# values：指定需要聚合的字段
# index：指定某些原始变量作为行索引
# columns：指定哪些离散的分组变量
# aggfunc：指定相应的聚合函数
# fill_value：使用一个常数替代缺失值，默认不替换
# margins：是否进行行或列的汇总，默认不汇总
# dropna：默认所有观测为缺失的列
# margins_name：默认行汇总或列汇总的名称为'All'

dic1 = {'Name': ['Liu', 'Zhang', 'L'], 'Weight': [61, 63, 65], 'Sex': ['M', 'F', 'M'], 'Age': [27, 23, 23],
        'Height': [165.7, 167.2, 180]}
dic2 = {'Name': ['LiuShunxiang', 'Zhangshan'], 'Sex': ['F', 'M'], 'Age': [27, 23], 'Height': [165.7, 167.2],
        'Weight': [61, 63]}
student1 = pd.DataFrame(dic1)
student2 = pd.DataFrame(dic2)

student3 = pd.concat([student1, student2])

dic4 = {'Name': ['Liu', 'Zhang', 'li'], 'Score': [61, 63, 80]}
score = pd.DataFrame(dic4)
stu_score = pd.merge(student3, score, how='outer')

t = pd.pivot_table(student3, values=['Height', 'Weight'], columns=['Sex', 'Age'],
                   aggfunc=[np.mean, np.median, np.std]).unstack()
print t

t1 = pd.pivot_table(student3, index=['Sex', 'Age'])
print t1
t2 = t1.ix[['F']]
print t2

score.plot()
pass
