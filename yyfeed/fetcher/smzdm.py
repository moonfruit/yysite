# -*- coding: utf-8 -*-
from typing import Text

# noinspection PyProtectedMember
from bs4 import SoupStrainer

from .base import FeedFetcher


class SmzdmFetcher(FeedFetcher):
    FILTER = SoupStrainer('article', 'article-details')

    def __init__(self, keywords=None):
        super().__init__()
        self.keywords = keywords

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

        return data

    # noinspection PyUnusedLocal
    def callback(self, result, item):
        title = result['title'].upper()
        goon = False

        if self.keywords:
            for word in self.keywords:
                if word in title:
                    goon = True
                    break

        else:
            goon = True

        if goon:
            result['id'] = result['link'].split('/')[-2]

        return goon
