# -*- coding: utf-8 -*-
import re

from django.contrib.syndication import views
from django.utils.feedgenerator import Atom1Feed

from yyfeed.models import APP_NAME, Feed, FeedItem


# noinspection PyMethodMayBeStatic
class RssFeed(views.Feed):
    # noinspection PyMethodOverriding
    def get_object(self, request, name):
        return Feed.objects.get(name=name)

    def title(self, obj: Feed):
        return obj.title

    def link(self, obj: Feed):
        return obj.link

    def description(self, obj: Feed):
        return obj.description

    def items(self, obj: Feed):
        return obj.feeditem_set.order_by('-publish_date', '-item_id')[:obj.limit]

    def item_guid(self, item: FeedItem):
        return item.feed.name + '-' + item.item_id

    def item_title(self, item: FeedItem):
        return item.title

    def item_description(self, item: FeedItem):
        return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]*', '', item.description)

    def item_link(self, item: FeedItem):
        return item.link


# noinspection PyMethodMayBeStatic
class AtomFeed(RssFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj: Feed):
        return obj.description

    def feed_guid(self, obj: Feed):
        return APP_NAME + '-' + obj.name
