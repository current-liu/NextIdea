#!/usr/bin/env python
# coding=utf-8
"""
Created on 10/31/17 1:34 AM

base Info
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

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


sale_orders = get_df_from_db(table_sale_orders)
sale_orders_products = get_df_from_db(table_sale_order_products)
catalog_product_items = get_df_from_db(table_catalog_product_items)
catalog_products = get_df_from_db(table_catalog_products)
cart = get_df_from_db(table_cart)

sale_orders = sale_orders[['id', 'status', 'payment_status', 'subtotal']].set_index('id')
sale_orders_products = sale_orders_products[
    ['id', 'order_id', 'sku', 'product_id', 'name', 'price', 'quantity']].set_index('id')

cart = cart[['id', 'product_id', 'sku_id']].set_index('id')

catalog_products = catalog_products[['id', 'category_id', 'created_by', 'created_at']].set_index('id', drop=False)
catalog_product_items = catalog_product_items[['id', 'product_id', 'sku', 'price']].set_index('id')

product_count_in_cart = cart.groupby(by='product_id').count()
product_count_in_cart.columns = ['num']
print product_count_in_cart

product_count_in_order = sale_orders_products[['product_id', 'sku']].groupby(by='product_id').count()
product_count_in_order.columns = ['num']
print product_count_in_order

# 购物车数量
product_count_added_in_cart = product_count_in_cart.add(product_count_in_order, fill_value=0)

catalog_product_info = pd.merge(catalog_products, catalog_product_items, how='outer', left_on='id',
                                right_on='product_id')

pass
