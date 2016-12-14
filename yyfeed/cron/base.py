# -*- coding: utf-8 -*-
import logging

from abc import ABCMeta, abstractmethod
from django.conf import settings

from yyfeed.fetcher import Fetcher
from yyfeed.models import Feed
from yyutil.code import build

logger = logging.getLogger(__name__)
cache = build(settings.YYFEED_CACHE)


class FetcherJob(metaclass=ABCMeta):
    FETCHER = Fetcher

    def do(self):
        # noinspection PyBroadException
        try:
            feed = Feed.objects.get(name=self.name())
            self.fetch(feed)

        except:
            logger.exception('Fetch error')

        return 'Success.'

    @abstractmethod
    def name(self):
        pass

    @staticmethod
    def fetch(feed: Feed):
        logger.debug('---- Start fetch feed [%s] ----', feed.name)

        fetcher = build(feed.fetcher)
        fetcher.cache = cache
        for item in fetcher.fetch():
            logger.trace("item = %s", item)

            feed.feeditem_set.update_or_create(
                item_id=item.id,
                defaults={
                    'title': item.title.trim(),
                    'publish_date': item.publish_date,
                    'link': item.link,
                    'description': item.description
                }
            )

        logger.debug('---- End fetch feed [%s] ----', feed.name)
