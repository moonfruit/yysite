# -*- coding: utf-8 -*-
from os.path import basename, splitext
from typing import Iterable

from bs4 import SoupStrainer

from yyfeed.fetcher import Fetcher
from yyfeed.fetcher import Item


class RosiyyFetcher(Fetcher):
    URL = 'http://www.rosiyy.com'
    FILTER = SoupStrainer('h2', 'entry_title')
    FILTER_CONTENT = SoupStrainer('div', 'post postimg')

    def fetch(self) -> Iterable[Item]:
        soup = self.fetcher.soup(self.URL, parse_only=self.FILTER)

        for a in soup.find_all('a'):
            link = a['href']
            uid = splitext(basename(link))[0]
            title = a.text
            description = self.description(link)
            if description:
                yield Item(uid, title, None, link, description)

    def description(self, url, page=None):
        loop = page is None
        max_page = 0

        if loop:
            data = self.cache.get(url)
            if data is not None:
                return data
        else:
            url += "?page=%d" % page

        soup = self.fetcher.soup(url, parse_only=self.FILTER_CONTENT)
        if not soup:
            return None

        soup = soup.div
        if loop:
            div = soup.find('div', 'archives_page_bar')
            max_page = 1
            for a in div:
                if 'next' in a.get('class', []):
                    break
                max_page = int(a.text)
            max_page += 1

        lines = []
        for p in soup.find_all('p'):
            a = p.a
            if a:
                img = a.img
                if img:
                    del img['height']
                    del img['width']
                    lines.append(str(p))
        content = '\n'.join(lines)

        if not loop:
            return content

        results = [content]
        for i in range(2, max_page):
            results.append(self.description(url, i))

        data = '\n'.join(results)
        self.cache.set(url, data)
        return data
