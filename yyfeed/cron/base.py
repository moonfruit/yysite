# -*- coding: utf-8 -*-
import logging
from abc import ABCMeta, abstractmethod

from django.conf import settings

from yyfeed.models import Feed
from yyutil.code import build

logger = logging.getLogger(__name__)
cache = build(settings.YYFEED_CACHE)


class FetcherJob(metaclass=ABCMeta):
    def do(self):
        name = self.name()

        try:
            Feed.objects.get(name=name).fetch()

        except Exception as e:
            logger.exception('Fetch error')
            logger.debug('---- Error fetch feed [%s] ----', name)
            raise e

        return 'Success.'

    @abstractmethod
    def name(self):
        pass
