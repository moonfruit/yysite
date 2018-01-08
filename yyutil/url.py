# -*- coding: utf-8 -*-
import json
import logging
from os.path import getmtime
from time import sleep
from typing import BinaryIO, Union
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request
from urllib.request import build_opener

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree

from .time import fromtimestamp, now

BAIDUSPIDER_USER_AGENT = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
FEEDLY_USER_AGENT = 'Feedly/1.0 (+http://www.feedly.com/fetcher.html; like FeedFetcher-Google)'

BROWSER = {
    'baiduspider': BAIDUSPIDER_USER_AGENT,
    'feedly': FEEDLY_USER_AGENT,
}

logger = logging.getLogger(__name__)

_ua = None


def user_agent(browser) -> str:
    result = BROWSER.get(browser)
    if result is None:
        global _ua
        if _ua is None:
            _ua = UserAgent(fallback=BAIDUSPIDER_USER_AGENT)
        else:
            try:
                delta = now() - fromtimestamp(getmtime(_ua.path))
                if delta.days >= 7:
                    _ua.update()
            except FileNotFoundError:
                pass

        result = _ua[browser]
    return result


class UrlFetcher:
    def __init__(self, headers=None, timeout=120, wait=0, browser='baiduspider', every_time=None):
        self.opener = build_opener(HTTPCookieProcessor())
        self.timeout = timeout
        self.wait = wait
        self.browser = browser
        self.every_time = every_time
        self.headers = {
            'Connection': 'close',
            'User-Agent': user_agent(browser)
        }
        if headers:
            self.headers.update(headers)

    def open(self, url, data=None) -> BinaryIO:
        if logger.isEnabledFor(logging.DEBUG):
            if self.wait > 0:
                logger.debug("Fetching [%s] after [%d] seconds", url, self.wait)
            else:
                logger.debug("Fetching [%s]", url)

        if self.every_time:
            headers = self.headers.copy()
            headers['User-Agent'] = user_agent(self.browser)

        else:
            headers = self.headers

        req = Request(url, headers=headers)
        if data:
            req.data = urlencode(data)

        if self.wait > 0:
            sleep(self.wait)

        return self.opener.open(req, timeout=self.timeout)

    def fetch(self, url, data=None, encoding='utf-8') -> str:
        with self.open(url, data) as stream:
            return stream.read().decode(encoding)

    def json(self, url, data=None, encoding='utf-8') -> Union[dict, list]:
        return json.loads(self.fetch(url, data, encoding))

    def soup(self, url, data=None, **kwargs) -> BeautifulSoup:
        with self.open(url, data) as stream:
            return BeautifulSoup(stream, 'lxml', **kwargs)

    def xml(self, url, data=None):
        with self.open(url, data) as stream:
            return etree.parse(stream)
