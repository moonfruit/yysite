# -*- coding: utf-8 -*-
from typing import Text

from bs4 import SoupStrainer

from yyfeed.fetcher.base import FeedFetcher


class TtrssFetcher(FeedFetcher):
    FILTER = SoupStrainer('div', 'context')
    FILTER_CONTENT = SoupStrainer('div', id='post_content')

    def __init__(self):
        super().__init__()
        self.fetcher.wait = 2

    def url(self) -> Text:
        return 'http://ttrss.com/feed'

    def description(self, url) -> Text:
        soup = self.cached_soup(url, parse_only=self.FILTER)
        results = []

        content = soup.find(self.FILTER_CONTENT)
        content = self.retrieve(content)
        results.append(content)

        pagelist = soup.find('div', 'pagelist')
        for a in pagelist.find_all('a'):
            link = a.get('href')
            if link:
                content = self.cached_soup(link, parse_only=self.FILTER_CONTENT)
                div = content.div
                if div:
                    content = self.retrieve(div)
                    results.append(content)

        return '\n'.join(results)

    # noinspection PyUnusedLocal
    @staticmethod
    def callback(result, item):
        title = result['title'].upper()
        return 'ROSI写真' not in title

    @staticmethod
    def retrieve(content):
        wumii = content.find('div', 'wumii-hook')
        if wumii:
            wumii.decompose()

        for img in content.find_all('img'):
            del img['height']
            del img['width']
            img['src'] = img['src'].replace('http://70.ot2.pw/p.php?url=', '')

        return str(content)
