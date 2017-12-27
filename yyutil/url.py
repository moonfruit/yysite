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

from .time import now, fromtimestamp

BAIDUSPIDER_USER_AGENT = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'

logger = logging.getLogger(__name__)
ua = UserAgent(fallback=BAIDUSPIDER_USER_AGENT)


class UrlFetcher:
    def __init__(self, headers=None, timeout=120, wait=0, random_user_agent=False):
        self.opener = build_opener(HTTPCookieProcessor())
        self.timeout = timeout
        self.wait = wait
        self.random_user_agent = random_user_agent
        self.headers = {
            'Connection': 'close',
            'User-Agent': BAIDUSPIDER_USER_AGENT
        }
        if headers:
            self.headers.update(headers)

    def open(self, url, data=None) -> BinaryIO:
        if logger.isEnabledFor(logging.DEBUG):
            if self.wait > 0:
                logger.debug("Fetching [%s] after [%d] seconds", url, self.wait)
            else:
                logger.debug("Fetching [%s]", url)

        if self.random_user_agent:
            try:
                delta = now() - fromtimestamp(getmtime(ua.path))
                if delta.days >= 7:
                    ua.update()

            except FileNotFoundError:
                pass

            headers = self.headers.copy()
            headers['User-Agent'] = ua.random

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
