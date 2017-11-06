#!/usr/bin/env
# coding:utf-8


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
    rows = text.split("\n")
    print rows
    table = []
    for row in rows:

        col_list = cols_to_dict(row)

        table.append(col_list)

    return JsonResponse(table , safe=False)


def cols_to_dict(row):
    cols = row.split("|")
    col_list = []

    for col in cols:

        col_list.append(col)

    # del col_list['col0']
    # del col_list['col' + str(m - 1)]
    return col_list
