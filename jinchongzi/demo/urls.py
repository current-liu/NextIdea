#!/usr/bin/env
# coding:utf-8

from django.conf.urls import url
from . import views, service

__author__ = 'liuchao'
__version__ = '1.0'

app_name = "demo"

urlpatterns = [url(r'^$', views.IndexView.as_view(), name='index'),
               url(r'^ajax/$', service.ajax, name='ajax'),
               url(r'^str_to_table/$', service.str_to_table, name='str_to_table'),



               ]
