# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import service
from django.test import TestCase


# Create your tests here.

class SalesTestCase(TestCase):
    def setUp(self):
        print ("======in setUp")

    def test_get_product_added_into_cart(self):
        time_begin = '2017-09-17 00:00:00'
        time_end = '2017-09-23 23:59:59'
        res = service.get_product_added_into_cart(time_begin, time_end)
        print res
