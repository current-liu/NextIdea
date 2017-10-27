#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/27/17 4:48 PM

base Info
"""
import numpy as np, pandas as pd
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

total_births = pd.pivot_table(names, index='year',values='births',columns='sex',aggfunc=np.sum, margins=False)
total_births.plot(title='Total births by sex and year')


def add_prop(group):
    births = group.births.astype(float)

    group['prop'] = births/births.sum()
    return group


names = names.groupby(['year','sex']).apply(add_prop)

print np.allclose(names.groupby(['year','sex']).prop.sum(), 1)


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)
pass
