#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/31/17 1:34 AM

base Info
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime

__author__ = 'liuchao'
__version__ = '1.0'

DB_CONNECT_STRING = 'mysql+pymysql://liuchao:1234@localhost/jollyhers?charset=utf8mb4'

table_sale_orders = "sale_orders"
table_sale_order_products = "sale_order_products"
table_catalog_product_items = "catalog_product_items"
table_catalog_products = "catalog_products"
table_cart = "cart"


def get_df_from_db(table):
    return pd.read_sql_table(table, DB_CONNECT_STRING)

"""Function: read data from database"""
sale_orders = get_df_from_db(table_sale_orders)
sale_orders_products = get_df_from_db(table_sale_order_products)
catalog_product_items = get_df_from_db(table_catalog_product_items)
catalog_products = get_df_from_db(table_catalog_products)
cart = get_df_from_db(table_cart)


"""Function: select values"""
sale_orders = sale_orders[['id', 'status', 'payment_status', 'subtotal', 'created_at', 'updated_at']]

sale_orders_products = sale_orders_products[
    ['id', 'order_id', 'sku', 'product_id', 'name', 'price', 'quantity']]

cart = cart[['id', 'product_id', 'sku_id','created_at']]
cart['created_at'] = cart['created_at'].astype('datetime64[ns]')

catalog_products = catalog_products[['id', 'category_id', 'created_by', 'created_at']]

catalog_product_items = catalog_product_items[['id', 'product_id', 'sku', 'price']]


"""Function: in specific period,product added into cart"""
# time_begin = datetime.datetime.strptime('2017-09-10 00:00:00', '%Y-%m-%d %H:%M:%S')
# time_end = datetime.datetime.strptime('2017-09-15 23:59:59', '%Y-%m-%d %H:%M:%S')

time_begin = '2017-09-10 00:00:00'
time_end = '2017-09-15 23:59:59'
cart_1 = cart.set_index(['created_at'], drop=False)
product_count_in_cart = cart_1[time_begin:time_end]
product_count_in_cart = product_count_in_cart[['product_id', 'sku_id']].groupby(by='product_id').count()
product_count_in_cart.columns = ['num']
print product_count_in_cart


sale_orders_info = pd.merge(sale_orders, sale_orders_products, how='outer', left_on='id', right_on='order_id')
sale_orders_info['created_at'] = sale_orders_info['created_at'].astype('datetime64[ns]')
sale_orders_info['updated_at'] = sale_orders_info['updated_at'].astype('datetime64[ns]')
sale_orders_info.set_index(['created_at'], inplace=True)
# print sale_orders_info
# print sale_orders_info.index
product_count_in_order = sale_orders_info[time_begin:time_end]
product_count_in_order = product_count_in_order[['product_id', 'sku']].groupby(by='product_id').count()
product_count_in_order.columns = ['num']
print product_count_in_order

# result
product_count_added_in_cart = product_count_in_cart.add(product_count_in_order, fill_value=0)
print product_count_added_in_cart


"""Product basic info"""
catalog_product_info = pd.merge(catalog_products, catalog_product_items, how='outer', left_on='id',
                                right_on='product_id')


"""Function: in specific period,product turned into pay status"""
sale_orders_info_pay = pd.merge(sale_orders, sale_orders_products, how='outer', left_on='id', right_on='order_id')
sale_orders_info_pay['created_at'] = sale_orders_info_pay['created_at'].astype('datetime64[ns]')
sale_orders_info_pay['updated_at'] = sale_orders_info_pay['updated_at'].astype('datetime64[ns]')
sale_orders_info_pay.set_index(['updated_at'], inplace=True)

time_pay_begin = '2017-09-10 00:00:00'
time_pay_end = '2017-09-15 23:59:59'
product_count_in_pay = sale_orders_info_pay[(sale_orders_info_pay['status'] == 'Paid')|(sale_orders_info_pay['status'] == 'Paid Processing')|(sale_orders_info_pay['status'] == 'Shipping')]

#result: in pay
product_count_in_pay = product_count_in_pay[time_pay_begin:time_pay_end]
print product_count_in_pay

#result: in paid
# TODO
pass
