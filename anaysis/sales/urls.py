#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/8/31 0031 上午 9:03

base Info
"""
from django.conf.urls import url
from . import views, service

__author__ = 'liuchao'
__version__ = '1.0'

app_name = "users"
# urlpatterns = [url(r'^$', views.index, name="index")]
urlpatterns = [
    url(r'^ajax/$', service.ajax, name='ajax'),
    url(r'^get_product_added_into_cart/$', service.get_product_added_into_cart, name='get_product_added_into_cart'),
    url(r'^get_product_basic_info/$', service.get_product_basic_info, name='get_product_basic_info'),
    url(r'^get_product_sale_info/$', service.get_product_sale_info, name='get_product_sale_info'),
    url(r'^anaysis_sale/$', service.anaysis_sale, name='anaysis_sale'),


]
