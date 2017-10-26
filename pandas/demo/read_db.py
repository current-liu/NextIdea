#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/26/17 10:40 AM

base Info
"""
import numpy as np, pandas as pd
import pymysql
from sqlalchemy import Column, String, create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

from config import DB_CONFIG
__author__ = 'liuchao'
__version__ = '1.0'

conn = pymysql.connect(**DB_CONFIG)

#.read_sql_query()
sql = "select * from sale_orders"
df = pd.read_sql_query(sql, conn)

#.read_sql_table()
DB_CONNECT_STRING = 'mysql+mysqldb://liuchao:1234@localhost/jollyhers?charset=utf8mb4'
engine = create_engine(DB_CONNECT_STRING,echo=True)
# DBSession = sessionmaker(bind=engine)
table_name = "sale_orders"
df1 = pd.read_sql_table(table_name, engine)
df2 = pd.read_sql_table(table_name, DB_CONNECT_STRING)


pass





