#!/usr/bin/env python
# coding=utf-8
"""
Created on 11/1/17 11:23 PM

base Info
"""
from django.http import HttpResponse, JsonResponse
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime

__author__ = 'liuchao'
__version__ = '1.0'


def ajax(request):
    n = request.GET.get("id")
    print n
    r = {"id": n}

    return JsonResponse(r)


DB_CONNECT_STRING = 'mysql+pymysql://liuchao:1234@192.168.220.130/jollyhers?charset=utf8mb4'

table_sale_orders = "sale_orders"
table_sale_order_products = "sale_order_products"
table_catalog_product_items = "catalog_product_items"
table_catalog_products = "catalog_products"
table_catalog_product_manufacturer = "catalog_product_manufacturer"
table_catalog_manufacturers = "catalog_manufacturers"
table_cart = "cart"


def get_df_from_db(table):
    return pd.read_sql_table(table, DB_CONNECT_STRING)


"""Function: read data from database"""
sale_orders = get_df_from_db(table_sale_orders)
sale_orders_products = get_df_from_db(table_sale_order_products)
catalog_product_items = get_df_from_db(table_catalog_product_items)
catalog_products = get_df_from_db(table_catalog_products)
catalog_product_manufacturer = get_df_from_db(table_catalog_product_manufacturer)
catalog_manufacturers = get_df_from_db(table_catalog_manufacturers)
cart = get_df_from_db(table_cart)

"""Function: select values"""
sale_orders = sale_orders[['id', 'status', 'payment_status', 'subtotal', 'created_at', 'updated_at']]
sale_orders['created_at'] = sale_orders['created_at'].astype('datetime64[ns]')

sale_orders_products = sale_orders_products[
    ['id', 'order_id', 'sku', 'product_id', 'name', 'price', 'quantity']]

cart = cart[['id', 'product_id', 'sku_id', 'quantity', 'created_at']]
cart['created_at'] = cart['created_at'].astype('datetime64[ns]')

catalog_products = catalog_products[['id', 'name', 'category_id', 'created_by', 'created_at', 'is_active']]
catalog_products['created_at'] = catalog_products['created_at'].astype('datetime64[ns]')
catalog_product_items = catalog_product_items[['id', 'product_id', 'sku', 'price']]
catalog_product_manufacturer = catalog_product_manufacturer[['id', 'product_id', 'manufacturer_id']]
catalog_manufacturers = catalog_manufacturers[['id', 'name']]


def get_product_added_into_cart(request):
    """Function: in specific period,product added into cart"""
    time_begin = request.GET.get('t1')
    time_end = request.GET.get('t2')
    product_id = request.GET.get('product_id')
    # time_begin = '2010-09-17 00:00:00'
    # time_end = '2021-01-01 00:00:00'
    # time_begin = datetime.datetime.strptime('2017-09-10 00:00:00', '%Y-%m-%d %H:%M:%S')
    # time_end = datetime.datetime.strptime('2017-09-15 23:59:59', '%Y-%m-%d %H:%M:%S')

    sale_orders_info = pd.merge(sale_orders, sale_orders_products, left_on='id', right_on='order_id')

    if (time_begin is None) | (time_end is None):
        product_count_in_cart = cart
        product_count_in_order = sale_orders_info
    else:
        cart_1 = cart.set_index(['created_at'], drop=False)
        product_count_in_cart = cart_1[time_begin:time_end]

        sale_orders_info['created_at'] = sale_orders_info['created_at'].astype('datetime64[ns]')
        sale_orders_info.set_index(['created_at'], inplace=True)
        product_count_in_order = sale_orders_info[time_begin:time_end]

    if product_id is None:
        product_count_in_cart = product_count_in_cart[['product_id', 'quantity']].groupby(by='product_id').sum()
        product_count_in_order = product_count_in_order[['product_id', 'quantity']].groupby(by='product_id').sum()
    else:
        product_count_in_cart = product_count_in_cart[product_count_in_cart['product_id'] == product_id]
        product_count_in_order = product_count_in_order[product_count_in_order['product_id' == product_id]]
    print product_count_in_cart
    print product_count_in_order

    # result
    product_count_added_in_cart = product_count_in_cart.add(product_count_in_order, fill_value=0)
    print product_count_added_in_cart

    product_count_added_in_cart.index.name = 'product_id'
    r = product_count_added_in_cart.reset_index().to_dict('index')
    return JsonResponse(r, safe=False)


def get_product_basic_info(request):
    """Product basic info"""
    sku = request.GET.get('sku')

    catalog_product_info = pd.merge(catalog_products, catalog_product_items[catalog_product_items['sku'] == sku],
                                    how='inner', left_on='id', right_on='product_id')
    print catalog_product_info
    print catalog_product_info.columns.tolist()
    r = catalog_product_info.drop(labels=['id_x', 'id_y'], axis=1).to_dict('index')
    return JsonResponse(r, safe=False)


def get_product_sale_info(request):
    """Function: in specific period,product turned into pay status"""
    time_begin = request.GET.get('t1')
    time_end = request.GET.get('t2')

    sale_orders['created_at'] = sale_orders['created_at'].astype('datetime64[ns]')
    # sale_orders['updated_at'] = sale_orders['updated_at'].astype('datetime64[ns]')
    sale_orders_period = sale_orders.set_index(['created_at'])
    sale_orders_period = sale_orders_period[time_begin:time_end]
    sale_orders_products['amount'] = sale_orders_products['price'] * sale_orders_products['quantity']
    sale_orders_info = pd.merge(sale_orders_period, sale_orders_products, how='inner', left_on='id',
                                right_on='order_id')

    # sale_orders_pivot = pd.pivot_table(sale_orders_info,index=['sku','order_id','status','payment_status'],values=['quantity','price','amount'])
    # time_pay_begin = '2017-09-17 00:00:00'
    # time_pay_end = '2017-09-23 23:59:59'

    # result: in pay

    product_count_in_ordered = sale_orders_info[
        (sale_orders_info['status'] == 'Paid') | (sale_orders_info['status'] == 'Paid Processing') | (
            sale_orders_info['status'] == 'Shipping') | (
            sale_orders_info['status'] == 'Issue')].sort_values('sku')
    product_count_in_ordered = product_count_in_ordered[['sku', 'quantity']].groupby(by='sku').sum()
    product_count_in_ordered.reset_index(inplace=True)
    product_count_in_ordered.columns = ['sku', 'ordered_quantity']
    # dict_product_count_in_paying = product_count_in_ordered.reset_index().to_dict('index')
    # print product_count_in_ordered
    # return JsonResponse(dict_product_count_in_paying, safe=False)


    # result: in paid
    # time_paid_begin = '2017-09-17 00:00:00'
    # time_paid_end = '2017-09-23 23:59:59'

    product_count_in_paid = sale_orders_info[(sale_orders_info['payment_status'] == 'Completed')]
    product_sales_count = pd.pivot_table(product_count_in_paid, values=['quantity', 'amount'], index='sku',
                                         aggfunc=np.sum)
    product_sales_count.columns = ['paid_amount', 'paid_quantity']
    product_sales_count.reset_index(inplace=True)

    # result: decimals
    res = pd.merge(product_count_in_ordered, product_sales_count)
    res['ordered_to_paid'] = res['paid_quantity'] / res['ordered_quantity']
    decimals = pd.Series([2, 2], index=['paid_amount', 'ordered_to_paid'])
    r = res.round(decimals).to_dict('index')
    return JsonResponse(r, safe=False)


def anaysis_sale(request):
    product_id = request.GET.get('product_id')
    try:
        manufacturer_id = int(request.GET.get('manufacturer_id'))
    except:
        manufacturer_id = None
    created_at = request.GET.get('created_at')
    created_by = request.GET.get('created_by')
    try:
        is_active = int(request.GET.get('is_active'))
    except:
        is_active = None
    try:
        category_id = int(request.GET.get('category_id'))
    except:
        category_id = None
    time_begin = request.GET.get('t1')
    time_end = request.GET.get('t2')

    catalog_product_info = pd.merge(catalog_products, catalog_product_items, left_on='id', right_on='product_id')
    catalog_product_info = pd.merge(catalog_product_info, catalog_product_manufacturer, left_on='product_id',
                                    right_on='product_id')
    catalog_product_info = catalog_product_info[
        ['product_id', 'sku', 'name', 'category_id', 'is_active', 'created_by', 'created_at', 'price',
         'manufacturer_id', ]]

    if product_id is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['product_id'] == product_id]
        pass
    if manufacturer_id is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['manufacturer_id'] == manufacturer_id]
        pass
    if created_at is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['created_at'] == created_at]
        pass
    if created_by is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['created_by'] == created_by]
        pass
    if is_active is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['is_active'] == is_active]
        pass
    if category_id is not None:
        catalog_product_info = catalog_product_info[catalog_product_info['category_id'] == category_id]
        pass

    product_id_list = catalog_product_info['product_id']
    product_added_into_cart = anaysis_product_added_into_cart(time_begin, time_end, product_id_list)
    product_sale_info = anaysis_product_sale_info(time_begin, time_end, product_id_list)
    res = pd.merge(catalog_product_info, pd.merge(product_added_into_cart, product_sale_info))

    decimals = pd.Series([2, 2], index=['paid_amount', 'ordered_to_paid'])
    return JsonResponse(res.round(decimals).to_dict('index'), safe=False)


def anaysis_product_added_into_cart(time_begin, time_end, product_id_list):
    """Function: in specific period,product added into cart"""

    sale_orders_products_1 = sale_orders_products[sale_orders_products['product_id'].isin(product_id_list)]
    cart_1 = cart[cart['product_id'].isin(product_id_list)]
    print "cart_1"
    print cart_1

    sale_orders_info = pd.merge(sale_orders, sale_orders_products_1, left_on='id', right_on='order_id')

    if (time_begin is None) | (time_end is None):
        product_count_in_cart = cart_1
        product_count_in_order = sale_orders_info
    else:
        cart_1 = cart_1.set_index(['created_at'], drop=False)
        product_count_in_cart = cart_1[time_begin:time_end].reset_index()

        # sale_orders_info['created_at'] = sale_orders_info['created_at'].astype('datetime64[ns]')
        sale_orders_info.set_index(['created_at'], inplace=True)
        product_count_in_order = sale_orders_info[time_begin:time_end].reset_index()

    print "product_count_in_cart"
    print product_count_in_cart
    # print product_count_in_order

    # result
    product_count_in_cart_mini = product_count_in_cart[['product_id', 'quantity']].groupby(by='product_id').sum()
    product_count_in_order_mini = product_count_in_order[['product_id', 'quantity']].groupby(by='product_id').sum()
    product_count_added_in_cart = product_count_in_cart_mini.add(product_count_in_order_mini, fill_value=0)

    product_count_added_in_cart.reset_index(inplace=True)
    product_count_added_in_cart.columns = ['product_id', "cart_quantity"]
    # print product_count_added_in_cart
    return product_count_added_in_cart


def anaysis_product_sale_info(time_begin, time_end, product_id_list):
    """Function: in specific period,product turned into pay status"""
    sale_orders_period = sale_orders.set_index(['created_at'])
    sale_orders_period = sale_orders_period[time_begin:time_end]

    sale_orders_products_1 = sale_orders_products[sale_orders_products['product_id'].isin(product_id_list)]
    sale_orders_products_1['amount'] = sale_orders_products_1['price'] * sale_orders_products_1['quantity']

    sale_orders_info = pd.merge(sale_orders_period, sale_orders_products_1, left_on='id', right_on='order_id')

    # result: in pay

    # product_count_in_ordered = sale_orders_info[
    #     (sale_orders_info['status'] == 'Paid') | (sale_orders_info['status'] == 'Paid Processing') | (
    #         sale_orders_info['status'] == 'Shipping') | (
    #         sale_orders_info['status'] == 'Issue')].sort_values('sku')

    status_list = ['Paid', 'Paid Processing', 'Shipping', 'Issue']
    product_count_in_ordered = sale_orders_info[sale_orders_info['status'].isin(status_list)]
    print product_count_in_ordered
    product_count_in_ordered = product_count_in_ordered[['product_id', 'quantity']].groupby(by='product_id').sum()
    print product_count_in_ordered
    product_count_in_ordered.reset_index(inplace=True)
    product_count_in_ordered.columns = ['product_id', 'ordered_quantity']
    # dict_product_count_in_paying = product_count_in_ordered.reset_index().to_dict('index')
    # print product_count_in_ordered
    # return JsonResponse(dict_product_count_in_paying, safe=False)


    # result: in paid
    # time_paid_begin = '2017-09-17 00:00:00'
    # time_paid_end = '2017-09-23 23:59:59'

    product_count_in_paid = sale_orders_info[(sale_orders_info['payment_status'] == 'Completed')]
    product_sales_count = pd.pivot_table(product_count_in_paid, values=['quantity', 'amount'], index='product_id',
                                         aggfunc=np.sum)
    product_sales_count.columns = ['paid_amount', 'paid_quantity']
    product_sales_count.reset_index(inplace=True)

    # result: decimals
    res = pd.merge(product_count_in_ordered, product_sales_count)
    res['ordered_to_paid'] = res['paid_quantity'] / res['ordered_quantity']
    # decimals = pd.Series([2, 2], index=['paid_amount', 'ordered_to_paid'])
    # r = res.round(decimals).to_dict('index')
    # return JsonResponse(r, safe=False)
    return res
