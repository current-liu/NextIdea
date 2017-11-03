# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# Create your views here.


def index(request):
    return HttpResponse("You are at the users index.")


class IndexView(generic.ListView):
    template_name = "users/index.html"

    def get_queryset(self):
        pass

