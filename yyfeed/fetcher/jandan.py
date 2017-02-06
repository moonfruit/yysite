# -*- coding: utf-8 -*-
from typing import Iterable

from bs4 import SoupStrainer

from .base import Fetcher, Item


class JandanFetcher(Fetcher):
    URL = 'http://jandan.net/ooxx'
    FILTER = SoupStrainer('ol', 'commentlist')

    def fetch(self, count=5) -> Iterable[Item]:
        current = 1
        for i in range(count):
            if i == 0:
                soup = self.fetcher.soup(self.URL)
                current = int(soup.find('span', 'current-comment-page').text[1: -1])
                ol = soup.find(self.FILTER)
                for item in self.generate(ol):
                    yield item

            else:
                current -= 1
                for item in self.fetch_page(current):
                    yield item

    def fetch_page(self, page) -> Iterable[Item]:
        url = '%s/page-%d' % (self.URL, page)
        ol = self.fetcher.soup(url, parse_only=self.FILTER)
        return self.generate(ol)

    @staticmethod
    def generate(ol) -> Iterable[Item]:
        for item in ol.find_all('li'):
            if not item.get('id'):
                continue

            text = item.find('div', 'text')
            a = text.find('span', 'righttext').a

            imgs = []
            for img in text.find_all('a', 'view_img_link'):
                src = img['href']
                if not src.startswith('http'):
                    src = 'http:' + src
                imgs.append('<div><img src="%s"/></div>' % src)

            if imgs:
                yield Item(a.text, a.text, None, a['href'], ''.join(imgs))
