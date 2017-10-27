#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/27/17 1:40 PM

base Info
    movielens
"""
import numpy as np, pandas as pd

__author__ = 'liuchao'
__version__ = '1.0'

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
movielens_path = "/home/liuchao/Documents/PycharmProject/NextIdea/pydata-book/datasets/movielens/"
users = pd.read_table(movielens_path + 'users.dat', sep='::', header=None, names=unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(movielens_path + 'ratings.dat', sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movielens_path + 'movies.dat', sep='::', header=None, names=mnames, engine='python')

data = pd.merge(pd.merge(ratings, users), movies)

mean_ratings = pd.pivot_table(data, values=['rating'], index=['title'], columns=['gender'], aggfunc=np.mean)
print "mean_ratings"
print mean_ratings

ratings_by_title = data.groupby('title').size()
print "ratings_by_title"
print ratings_by_title

active_titles = ratings_by_title.index[ratings_by_title >= 250]
mean_active = mean_ratings.ix[active_titles]
print "mean_active"
print mean_active


c0 = mean_active.columns
c1 = mean_active.columns.values

"""Merge MultiIndex columns together into 1 level [duplicate]"""
"https://stackoverflow.com/questions/14507794/python-pandas-how-to-flatten-a-hierarchical-index-in-columns"
mean_active.columns = [' '.join(col).strip() for col in mean_active.columns.values]

print mean_active
top_female_ratings = mean_active.sort_values(by=['rating F','rating M'], ascending=False)
print "top_female_ratings"
print top_female_ratings


mean_active['diff'] = mean_active['rating M'] - mean_active['rating F']
sorted_by_diff = mean_active.sort_values(by='diff')
print "sorted_by_diff"
print sorted_by_diff

print mean_active


rating_std_by_title = data.groupby('title')['rating'].std()
print rating_std_by_title.ix[active_titles].sort_values(ascending=False)[:10]
pass
