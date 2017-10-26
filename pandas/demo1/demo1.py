#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/26/17 1:53 PM

base Info
"""
import matplotlib
import numpy as np, pandas as pd
import pymysql
from sqlalchemy import Column, String, create_engine


from config import DB_CONFIG
__author__ = 'liuchao'
__version__ = '1.0'

conn = pymysql.connect(**DB_CONFIG)

#.read_sql_query()
sql = "select * from sale_orders"
df1 = pd.read_sql_query(sql, conn)

#.read_sql_table()
DB_CONNECT_STRING = 'mysql+mysqldb://liuchao:1234@localhost/jollyhers?charset=utf8mb4'
engine = create_engine(DB_CONNECT_STRING,echo=False)

table_name = "sale_orders"
t_name = "sale_order_visitors"
df2 = pd.read_sql_table(table_name, engine)
df_sale_order_visitors = pd.read_sql_table(t_name, engine)

# t = pd.pivot_table(df2, index=['customer_id'])
t = df2.set_index(['customer_id','customer_firstname','customer_lastname'])

t1 = pd.pivot_table(df2, index=['customer_id','status','payment_status'])
# t.plot()
# print t1
sale_orders_mini = df2[['id','status','payment_status','total_paid']]
t3 = df2.ix[:,['id','status','payment_status']]
# print t3

df_sale_order_visitors_mini = df_sale_order_visitors.ix[:,['id','order_id','ip','location','os','lang']]

tab = df_sale_order_visitors_mini.merge(sale_orders_mini,left_on='order_id',right_on='id',how='outer')

tab_paid = tab[tab["total_paid"] > 0].sort_values(by=['total_paid'], ascending=False)
tab_1 = pd.pivot_table(tab_paid,index=['lang'],values=['total_paid'],aggfunc=[np.sum,np.mean,np.median])
print tab_1
tab_1.sort_values(by=['sum/total_paid'], ascending=False).plot(kind="barh")
pass





