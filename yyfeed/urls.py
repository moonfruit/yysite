# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles.storage import staticfiles_storage as storage
from django.views.generic import RedirectView

from . import views
from .models import APP_NAME
from .views import AtomFeed, RssFeed

feed = RssFeed()

app_name = APP_NAME
urlpatterns = [
    url(r'^favicon.ico$',
        RedirectView.as_view(url=storage.url("/yyfeed/favicon.ico"), permanent=True),
        name='favicon'
        ),
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^feed/(?P<name>\w+)/$', feed, name='feed'),
    url(r'^feed/(?P<name>\w+)/rss/$', feed, name='feed'),
    url(r'^feed/(?P<name>\w+)/atom/$', AtomFeed(), name='feed'),
]
