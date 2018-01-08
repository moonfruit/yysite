# -*- coding: utf-8 -*-
import re
from typing import Iterable, Text
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import BaseHandler

import execjs
from bs4 import BeautifulSoup, SoupStrainer

from .base import FeedFetcher, Item


class IAppsFetcher(FeedFetcher):
    DOMAIN = 'www.iapps.im'
    FILTER = SoupStrainer('div', id='articleLeft')

    def __init__(self):
        super().__init__()
        self.handler = BrowserHandler(self.DOMAIN)
        self.fetcher.opener.add_handler(self.handler)
        self.fetcher.headers['User-Agent'] = 'Feedly/1.0 (+http://www.feedly.com/fetcher.html; like FeedFetcher-Google)'
        self.fetcher.wait = 5
        # self.fetcher.random_user_agent = True

    def fetch(self) -> Iterable[Item]:
        try:
            self.fetcher.fetch(self.url())

        except HTTPError:
            url = self.handler.url
            if url:
                self.fetcher.open(url).close()

        finally:
            self.handler.url = None

        return super().fetch()

    def url(self) -> Text:
        return 'http://%s/feed' % self.DOMAIN

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


class BrowserHandler(BaseHandler):
    handler_order = 999  # after all other processing

    def __init__(self, domain):
        self.domain = domain
        self.url = None

    def check(self, response):
        soup = BeautifulSoup(response, 'lxml')

        script = soup.find('script')
        lines = ['function run() {', 'var a = {};']
        for line in script.text.splitlines():
            line = line.strip()
            if re.match('^var [^a]', line):
                lines.append(line)
            elif line.startswith(';'):
                lines.append('t = "%s";' % self.domain)
                lines.append(line)
        lines.append('return a.value;}')
        script = '\n'.join(lines)
        value = execjs.compile(script).call('run')

        data = {}
        form = soup.find('form')
        for item in form.find_all('input'):
            data[item['name']] = item.get('value', value)

        return 'http://%s%s?%s' % (self.domain, form['action'], urlencode(data))

    # noinspection PyUnusedLocal
    def http_response(self, request, response):
        if response.code == 503:
            self.url = self.check(response)
        return response

    https_response = http_response
