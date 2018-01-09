# -*- coding: utf-8 -*-
from os.path import basename, splitext
from typing import Iterable

# noinspection PyProtectedMember
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
            original_id = uid = splitext(basename(link))[0]
            original_title = title = a.text

            for index, description in enumerate(self.descriptions(link), 1):
                if description:
                    uid = "%s+%03d+%03d" % (original_id, 1000 - index, index)
                    if index > 1:
                        title = "%s（%d）" % (original_title, index)
                yield Item(uid, title, None, link, description)

    def descriptions(self, url):
        soup, description = self.content(url)
        if description:
            yield description

        if soup:
            pagelist = soup.find('div', 'archives_page_bar')
            if pagelist:
                for a in pagelist.find_all('a'):
                    if 'class' not in a:
                        _, description = self.content(a['href'])
                        if description:
                            yield description

    def content(self, url):
        soup = self.fetcher.soup(url, parse_only=self.FILTER_CONTENT)
        description = None
        if soup:
            imgs = []
            for img in soup.find_all('img'):
                del img['height']
                del img['width']
                if img['src'].startswith('/'):
                    img['src'] = self.URL + img['src']
                imgs.append(str(img))
            if imgs:
                description = '<div>' + '</div>\n<div>'.join(imgs) + '</div>'
        return soup, description
