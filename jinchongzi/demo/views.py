# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import HttpResponse
from django.views import generic
# Create your views here.


def index(request):
    return HttpResponse("You are at the demo index.")


class IndexView(generic.ListView):
    template_name = "demo/index.html"

    def get_queryset(self):
        pass

