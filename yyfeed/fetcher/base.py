# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Sequence

from yyutil.cache import Cache, DummyCache
from yyutil.url import UrlFetcher

Item = namedtuple('Item', 'id title publish_date link description')


class Fetcher(metaclass=ABCMeta):
    def __init__(self, cache: Cache = DummyCache()):
        self._fetcher = UrlFetcher()
        self._cache = cache

    @property
    def fetcher(self):
        return self._fetcher

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, cache):
        self._cache = cache

    @abstractmethod
    def fetch(self) -> Sequence[Item]:
        pass
