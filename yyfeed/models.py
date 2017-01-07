# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

APP_NAME = 'yyfeed'
ID_SIZE = 32
DESC_SIZE = 4000


class Feed(models.Model):
    name = models.CharField(max_length=ID_SIZE, unique=True)
    title = models.CharField(max_length=DESC_SIZE)
    fetcher = models.CharField(max_length=DESC_SIZE)
    link = models.CharField(max_length=DESC_SIZE)
    description = models.CharField(max_length=DESC_SIZE)

    def __str__(self):
        return self.title


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=ID_SIZE)
    title = models.CharField(max_length=DESC_SIZE)
    publish_date = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=DESC_SIZE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = ["feed", "item_id"]

    def __str__(self):
        return self.title
