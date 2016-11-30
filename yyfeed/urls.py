#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'yyfeed'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
