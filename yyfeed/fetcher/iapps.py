# -*- coding: utf-8 -*-
from typing import Text

from bs4 import SoupStrainer

from .base import FeedFetcher


class IAppsFetcher(FeedFetcher):
    FILTER = SoupStrainer('div', id='articleLeft')

    def __init__(self):
        super().__init__()
        self.fetcher.headers['User-agent'] =\
            'Feedly/1.0 (+http://www.feedly.com/fetcher.html; like FeedFetcher-Google)'
        self.fetcher.wait = 3

    def url(self) -> Text:
        return 'http://www.iapps.im/feed'

    def description(self, url) -> Text:
        data = ''
        soup = self.fetcher.soup(url, parse_only=self.FILTER)

        content = soup.find('div', 'entry-content')
        a = content.find('a', 'chat-btn')
        if a:
            a.extract()
        data += str(content)

        carousel = soup.find('div', 'carousel')
        if carousel:
            data += str(carousel)

        self.cache.set(url, data)
        return data

    # noinspection PyUnusedLocal
    @staticmethod
    def callback(result, item):
        result['id'] = result['link'].split('/')[-1]
        return True
