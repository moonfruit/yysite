# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Iterable

# noinspection PyProtectedMember
from bs4 import SoupStrainer

from yyfeed.fetcher import Item
from yyfeed.fetcher.base import Fetcher
from yyutil.time import astimezone


class TtrssFetcher(Fetcher):
    URL = 'https://ttrss.com/'
    FILTER = SoupStrainer('div', 'featured-media')
    FILTER_ARTICLE = SoupStrainer('article')
    FILTER_CONTENT = SoupStrainer('div', 'entry-content')

    def fetch(self) -> Iterable[Item]:
        pages = self.fetcher.soup(self.URL, parse_only=self.FILTER)
        for page in pages.find_all(self.FILTER):
            page = page.a['href']
            yield self.fetch_page(page)

    def fetch_page(self, page) -> Item:
        article = self.fetcher.soup(page, parse_only=self.FILTER_ARTICLE)

        header = article.header
        title = header.h1.text
        date = header.find('span', 'posted-on').text
        date = astimezone(datetime.strptime(date, '%Y-%m-%d'))

        imgs = []
        content = article.find(self.FILTER_ARTICLE)
        for img in content.find_all('img'):
            imgs.append('<div><img src="%s"/></div>' % img['src'])

        return Item(page, title, date, page, ''.join(imgs))
