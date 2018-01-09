# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Text

from bs4 import BeautifulSoup

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
    def fetch(self) -> Iterable[Item]:
        pass

    def cached_soup(self, url, parse_only=None):
        key = self.__class__.__name__ + '+' + url

        soup = self.cache.get(key)
        if soup is not None:
            return BeautifulSoup(soup, 'lxml')

        if parse_only is None:
            soup = self.fetcher.soup(url)
        else:
            soup = self.fetcher.soup(url, parse_only=parse_only)

        self.cache.set(key, str(soup))
        return soup


class FeedFetcher(Fetcher, metaclass=ABCMeta):
    DATE_TZ_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
    DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'

    callback = None

    def fetch(self) -> Iterable[Item]:
        root = self.fetcher.xml(self.url())

        for item in root.iter('item'):
            item = self.item(item)
            if item:
                yield item

    def item(self, item) -> Optional[Item]:
        result = self.build_result(item)

        if callable(self.callback):
            if not self.callback(result, item):
                return None

        result['description'] = self.cached_description(result['link'])

        return Item(**result)

    def build_result(self, item) -> Dict[Text, Any]:
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
                        result['publish_date'] = astimezone(datetime.strptime(child.text, self.DATE_FORMAT))

                    except ValueError:
                        result['publish_date'] = None

            elif child.tag == 'description':
                result['description'] = child.text

        return result

    def cached_description(self, url):
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


class MultiFeedFetcher(FeedFetcher, metaclass=ABCMeta):

    def fetch(self) -> Iterable[Item]:
        root = self.fetcher.xml(self.url())

        for item in root.iter('item'):
            for element in self.items(item):
                yield element

    def items(self, item) -> Iterable[Item]:
        result = self.build_result(item)

        if callable(self.callback):
            if not self.callback(result, item):
                return

        original_id = result['id']
        original_title = result['title']
        for index, description in enumerate(self.cached_description(result['link']), 1):
            if index > 1:
                result['id'] = "%s+%d" % (original_id, index)
                result['title'] = "%s（%d）" % (original_title, index)
            result['description'] = description
            yield Item(**result)

    @abstractmethod
    def description(self, link) -> List[Text]:
        pass
