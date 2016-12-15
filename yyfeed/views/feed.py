# -*- coding: utf-8 -*-
from django.contrib.syndication import views
from django.utils.feedgenerator import Atom1Feed

from yyfeed.models import Feed, FeedItem


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
        return obj.feeditem_set.order_by('-publish_date')[:30]

    def item_title(self, item: FeedItem):
        return item.title

    def item_description(self, item: FeedItem):
        return item.description

    def item_link(self, item: FeedItem):
        return item.link


class AtomFeed(RssFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj: Feed):
        return obj.description
