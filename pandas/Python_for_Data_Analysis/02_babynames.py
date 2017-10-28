#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/27/17 4:48 PM

base Info
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import pydata_book_datasets_path as datasets

__author__ = 'liuchao'
__version__ = '1.0'

babynames = datasets + '/babynames'
names1880 = pd.read_csv(babynames + '/yob1880.txt', names=['name', 'sex', 'birth'])
print names1880.groupby(by='sex', as_index=True).sum()

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = babynames + '/yob%d.txt' % year
    df = pd.read_csv(path, names=columns)
    df['year'] = year
    pieces.append(df)

names = pd.concat(pieces, ignore_index=True)

total_births = pd.pivot_table(names, index='year', values='births', columns='sex', aggfunc=np.sum, margins=False)
total_births.plot(title='Total births by sex and year')


def add_prop(group):
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)


# print np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
print "top1000"
print top1000

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = pd.pivot_table(top1000, index='year', values='births', columns='name', aggfunc=np.sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=False, figsize=(12, 10), grid=False, title="Number of birth per year")

table_1000_prop = pd.pivot_table(top1000, index="year", values='prop', columns="sex", aggfunc=np.sum)
table_1000_prop.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13),
                     xticks=range(1880, 2020, 10))

boys_2010_prop_cumsum = boys[boys.year == 2010].sort_values(by='prop', ascending=False).prop.cumsum()
boys_1900_prop_cumsum = boys[boys.year == 1900].sort_values(by='prop', ascending=False).prop.cumsum()

print boys_2010_prop_cumsum.searchsorted(0.5)
print boys_1900_prop_cumsum.searchsorted(0.5)


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    p = group.prop.cumsum().searchsorted(q)[0] + 1
    return p


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title="Number of popular names in top 50%")

get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
names['last_letters'] = last_letters
table = pd.pivot_table(names, index='last_letters', values='births', columns=['sex', 'year'], aggfunc=np.sum)
subtable_3_year = table.reindex(columns=[1910, 1960, 2010], level='year')
print subtable_3_year.head()
print subtable_3_year.sum()

letter_prop = subtable_3_year / subtable_3_year.sum().astype(float)
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend='False')

dny_ts = (table / table.sum().astype(float)).ix[['d', 'n', 'y'], 'M'].T
dny_ts.plot()

all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]

filtered = top1000[top1000.name.isin(lesley_like)]

filtered_sum = pd.pivot_table(filtered, index='year', values='births', columns='sex', aggfunc=np.sum)
filtered_sum_div = filtered_sum.div(filtered_sum.sum(1), axis=0)
filtered_sum_div.plot(style={'M': 'k-', 'F': 'k--'})

pass
