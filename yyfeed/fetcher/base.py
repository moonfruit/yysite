# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from datetime import datetime
from typing import Optional, Sequence, Text

from yyutil.cache import DummyCache
from yyutil.time import astimezone
from yyutil.url import UrlFetcher

Item = namedtuple('Item', 'id title publish_date link description')


class Fetcher(metaclass=ABCMeta):
    def __init__(self):
        self._fetcher = UrlFetcher()
        self._cache = DummyCache()

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


class FeedFetcher(Fetcher, metaclass=ABCMeta):
    DATE_TZ_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
    DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'

    callback = None

    def fetch(self) -> Sequence[Item]:
        root = self.fetcher.xml(self.url())

        results = []
        for item in root.iter('item'):
            item = self.item(item)
            if item:
                results.append(item)

        return results

    def item(self, item) -> Optional[Item]:
        result = {}
        for child in item:
            if child.tag == 'guid':
                result['id'] = child.text

            elif child.tag == 'title':
                result['title'] = child.text

            elif child.tag == 'link':
                result['link'] = child.text

            elif child.tag == 'pubDate':
                try:
                    result['publish_date'] = datetime.strptime(child.text, self.DATE_TZ_FORMAT)

                except ValueError:
                    try:
                        result['publish_date'] = astimezone(
                            datetime.strptime(child.text, self.DATE_FORMAT))

                    except ValueError:
                        result['publish_date'] = None

            elif child.tag == 'description':
                result['description'] = child.text

        if callable(self.callback):
            if not self.callback(result, item):
                return None

        result['description'] = self.cached_description(result['link'])

        return Item(**result)

    def cached_description(self, url) -> Text:
        data = self.cache.get(url)
        if data is not None:
            return data

        data = self.description(url)
        self.cache.set(url, data)
        return data

    @abstractmethod
    def url(self) -> Text:
        pass

    @abstractmethod
    def description(self, url) -> Text:
        pass
