# -*- coding: utf-8 -*-
from typing import Text

from bs4 import SoupStrainer

from .base import FeedFetcher


class SmzdmFetcher(FeedFetcher):
    FILTER = SoupStrainer('article', 'article-details')
    KEYWORDS = ['LEGO', 'lego', '乐高', '小米']

    def url(self) -> Text:
        return 'http://feed.smzdm.com'

    def description(self, url) -> Text:
        data = ''
        soup = self.fetcher.soup(url, parse_only=self.FILTER)

        link = soup.find('div', 'buy')
        if link:
            data += str(link)

        item = soup.find('div', 'item-box')
        if item:
            data += str(item)

        self.cache.set(url, data)
        return data

    # noinspection PyUnusedLocal
    def callback(self, result, item):
        title = result['title']
        goon = False
        for word in self.KEYWORDS:
            if word in title:
                goon = True
                break

        if goon:
            result['id'] = result['link'].split('/')[-2]

        return goon
