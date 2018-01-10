# -*- coding: utf-8 -*-
from django.db.models import CASCADE
from django.db.models import CharField, DateTimeField, ForeignKey, Model, PositiveIntegerField, TextField, URLField
from django.utils import timezone

APP_NAME = 'yyfeed'
ID_SIZE = 128
DESC_SIZE = 4000


class Feed(Model):
    name = CharField(max_length=ID_SIZE, unique=True)
    title = CharField(max_length=DESC_SIZE)
    fetcher = CharField(max_length=DESC_SIZE)
    link = URLField(max_length=DESC_SIZE)
    description = CharField(max_length=DESC_SIZE)
    limit = PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class FeedItem(Model):
    feed = ForeignKey(Feed, on_delete=CASCADE)
    item_id = CharField(max_length=ID_SIZE)
    title = CharField(max_length=DESC_SIZE)
    publish_date = DateTimeField(default=timezone.now)
    link = URLField(max_length=DESC_SIZE)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        index_together = ["feed", "item_id"]

    def __str__(self):
        return self.title
