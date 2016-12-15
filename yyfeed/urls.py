# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from .views import AtomFeed, RssFeed

feed = RssFeed()

app_name = 'yyfeed'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^feed/(?P<name>\w+)/$', feed),
    url(r'^feed/(?P<name>\w+)/rss/$', feed),
    url(r'^feed/(?P<name>\w+)/atom/$', AtomFeed()),
]
