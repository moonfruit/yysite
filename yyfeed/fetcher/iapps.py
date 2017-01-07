# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Sequence

from bs4 import SoupStrainer

from .base import Fetcher, Item


class IAppsFetcher(Fetcher):
    URL = 'http://www.iapps.im/feed'
    DATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
    FILTER = SoupStrainer('div', id='articleLeft')

    def fetch(self) -> Sequence[Item]:
        root = self.fetcher.xml(self.URL)

        results = []
        for item in root.iter('item'):
            results.append(self.item(item))

        return results

    def item(self, item):
        result = {}
        for child in item:
            if child.tag == 'title':
                result['title'] = child.text

            elif child.tag == 'link':
                result['id'] = child.text.split('/')[-1]
                result['link'] = child.text

            elif child.tag == 'pubDate':
                try:
                    result['publish_date'] = datetime.strptime(child.text, self.DATE_FORMAT)
                except ValueError:
                    result['publish_date'] = None

        result['description'] = self.description(result['link'])

        return Item(**result)

    def description(self, url):
        data = self.cache.get(url)
        if data is not None:
            return data

        soup = self.fetcher.soup(url, parse_only=self.FILTER)

        content = soup.find('div', 'entry-content')
        a = content.find('a', 'chat-btn')
        if a:
            a.extract()
        data = str(content)

        carousel = soup.find('div', 'carousel')
        if carousel:
            data += str(carousel)

        self.cache.set(url, data)
        return data
