#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/25/17 2:04 PM

base Info
"""
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

dic1 = {'Name': ['Liu', 'Zhang'], 'Weight': [61, 63], 'Sex': ['M', 'F'], 'Age': [27, 23],
        'Height': [165.7, 167.2]}
dic2 = {'Name': ['LiuShunxiang', 'Zhangshan'], 'Sex': ['F', 'M'], 'Age': [27, 23], 'Height': [165.7, 167.2],
        'Weight': [61, 63]}
student1 = pd.DataFrame(dic1)
student2 = pd.DataFrame(dic2)
print student1
print student2

# add rows
student3 = pd.concat([student1, student2])
# pd.DataFrame(student2,columns=['Age','Height','Name','Sex','Weight','Score'])
print student2

# add a column
student2.insert(5, "Score", [1, 2])

# update
student1.ix[student1['Name'] == 'Liu', 'Height'] = 192

# groupby
print student3.groupby('Sex').mean()
print student3.drop('Age', axis=1).groupby('Sex').mean()
print student3

t = student3.groupby(['Age', 'Sex']).mean()
t1 = student3.groupby(['Age', 'Sex']).agg([np.mean, np.median])

# order
series = pd.Series(np.array(np.random.randint(1, 20, 10)))
print series.sort_values()
print series.sort_index()
print student3.sort_values(by=['Sex', 'Age'])
print student3.sort_values(by=['Age', 'Sex'])

# join
dic4 = {'Name': ['Liu', 'Zhang', 'li'], 'Score': [61, 63, 80]}
score = pd.DataFrame(dic4)
stu_score = pd.merge(student3, score, how='outer')

pass
