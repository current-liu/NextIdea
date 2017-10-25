#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 4:06 PM

base Info
"""
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

"""
    删除法：当数据中的某个变量大部分值都是缺失值，可以考虑删除改变量；
        当缺失值是随机分布的，且缺失的数量并不是很多是，也可以删除这些缺失的观测。
    替补法：对于连续型变量，如果变量的分布近似或就是正态分布的话，可以用均值
        替代那些缺失值；如果变量是有偏的，可以使用中位数来代替那些缺失值；对于离
        散型变量，我们一般用众数去替换那些存在缺失的观测。
    插补法：插补法是基于蒙特卡洛模拟法，结合线性模型、广义线性模型、决策树等方
        法计算出来的预测值替换缺失值。
"""
dic1 = {'Name': ['Liu', 'Zhang'], 'Weight': [61, 63], 'Sex': ['M', 'F'], 'Age': [27, 23],
        'Height': [165.7, 167.2]}
dic2 = {'Name': ['LiuShunxiang', 'Zhangshan'], 'Sex': ['F', 'M'], 'Age': [27, 23], 'Height': [165.7, 167.2],
        'Weight': [61, 63]}
student1 = pd.DataFrame(dic1)
student2 = pd.DataFrame(dic2)

student3 = pd.concat([student1, student2])

dic4 = {'Name': ['Liu', 'Zhang', 'li'], 'Score': [61, 63, 80]}
score = pd.DataFrame(dic4)
stu_score = pd.merge(student3, score, how='outer')


s = stu_score['Score']
print sum(pd.isnull(s))
t = s.dropna()
print s
print stu_score.dropna()

print s.fillna(0)
t1 = s.fillna(method='ffill')
t2 = s.fillna(method='bfill')

stu_score_fix = stu_score.fillna({'Age':-1,'Height':-1,'Sex':'unknown','Weight':'unknown','Score':'-1'})

stu_score_mean = stu_score['Score'].mean()
pass
