# -*- coding: utf-8 -*-
from typing import List, Text

# noinspection PyProtectedMember
from bs4 import SoupStrainer

from yyfeed.fetcher.base import MultiFeedFetcher


class TtrssFetcher(MultiFeedFetcher):
    FILTER = SoupStrainer('div', 'content')
    FILTER_CONTENT = SoupStrainer('article', 'article-content')

    def __init__(self):
        super().__init__()
        self.fetcher.wait = 2

    def url(self) -> Text:
        return 'http://ttrss.com/feed'

    def description(self, url) -> List[Text]:
        soup = self.cached_soup(url, parse_only=self.FILTER)
        results = []

        article = soup.find(self.FILTER_CONTENT)
        self.retrieve_to(article, results)

        pagelist = soup.find('div', 'article-paging')
        if pagelist:
            for a in pagelist.find_all('a'):
                link = a.get('href')
                if link:
                    article = self.cached_soup(link, parse_only=self.FILTER_CONTENT)
                    self.retrieve_to(article, results)

        return results

    # noinspection PyUnusedLocal
    @staticmethod
    def callback(result, item):
        title = result['title'].upper()
        return 'ROSI写真' not in title

    @staticmethod
    def retrieve_to(article, results):
        imgs = []
        for img in article.find_all('img'):
            imgs.append(str(img))
        if imgs:
            results.append('<div>' + '</div>\n<div>'.join(imgs) + '</div>')
