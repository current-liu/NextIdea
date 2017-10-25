#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 11:25 AM

base Info
"""
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

t = np.random.seed(1234)
d1 = pd.Series(2 * np.random.normal(size=100) + 3)
d2 = np.random.f(2, 4, size=100)
d3 = np.random.randint(1, 100, size=100)

d1.count()  # 非空元素计算
d1.min()  # 最小值
d1.max()  # 最大值
d1.idxmin()  # 最小值的位置，类似于R中的which.min函数
d1.idxmax()  # 最大值的位置，类似于R中的which.max函数
d1.quantile(0.1)  # 10%分位数
d1.sum()  # 求和
d1.mean()  # 均值
d1.median()  # 中位数
d1.mode()  # 众数
d1.var()  # 方差
d1.std()  # 标准差
d1.mad()  # 平均绝对偏差
d1.skew()  # 偏度
d1.kurt()  # 峰度
print d1.describe()  # 一次性输出多个描述性统计指标


def stats(x):
    return pd.Series([x.count(), x.min(), x.idxmin(),
                      x.quantile(.25), x.median(),
                      x.quantile(.75), x.mean(),
                      x.max(), x.idxmax(),
                      x.mad(), x.var(),
                      x.std(), x.skew(), x.kurt()],
                     index=['Count', 'Min', 'Which_Min',
                            'Q1', 'Median', 'Q3', 'Mean',
                            'Max', 'Which_Max', 'Mad',
                            'Var', 'Std', 'Skew', 'Kurt'])


res = stats(d1)

df = pd.DataFrame(np.array([d1, d2, d3]).T, columns=['x1', 'x2', 'x3'])
print df.head()
res1 = df.apply(stats)
pass
