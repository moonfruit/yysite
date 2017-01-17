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
        try:
            feed = Feed.objects.get(name=self.name())
            self.fetch(feed)

        except Exception as e:
            logger.exception('Fetch error')
            raise e

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

            defaults = {
                'title': item.title.strip(),
                'link': item.link,
                'description': item.description.strip()
            }

            if item.publish_date:
                defaults['publish_date'] = item.publish_date

            feed.feeditem_set.update_or_create(item_id=item.id, defaults=defaults)

        logger.debug('---- End fetch feed [%s] ----', feed.name)
