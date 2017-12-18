# -*- coding: utf-8 -*-
import logging

from django.conf import settings

from yyutil.code import build
from . import Feed

logger = logging.getLogger(__name__)
cache = build(settings.YYFEED_CACHE)


def fetch(feed: Feed):
    logger.debug('---- Start fetch feed [%s] ----', feed.name)

    fetcher = build(feed.fetcher)
    fetcher.cache = cache
    count = 0
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
        count += 1

    logger.debug('---- End fetch feed [%s] with [%d] ----', feed.name, count)
    return count


Feed.fetch = fetch
