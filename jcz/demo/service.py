#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/9/1 0001 上午 9:31

base Info
"""

from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core import serializers




__author__ = 'liuchao'
__version__ = '1.0'


def ajax(request):

    n = request.GET.get("id")
    print n
    ret = {'status': True, 'error': "null"}
    l = [1, 2, 3, 4, 5]
    r = {"l": n}


    return JsonResponse(r)


def str_to_table(request):
    text = request.GET.get("str")
    rows = text.split("\r\n")
    print rows
    for row in rows:
        n = rows.index(row)
        cols = row.split("|")


        print cols

    return JsonResponse({"text" : text})


def cols_to_dict(cols):
    col_dict = {}
    for col in cols:
        m = cols.index(col)
        col_dict.append()