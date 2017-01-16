# -*- coding: utf-8 -*-
import json
from time import sleep
from typing import BinaryIO, Union
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request
from urllib.request import build_opener

from bs4 import BeautifulSoup
from lxml import etree


class UrlFetcher:
    def __init__(self, headers=None, timeout=30, wait=0):
        self.opener = build_opener(HTTPCookieProcessor())
        self.timeout = timeout
        self.wait = wait
        self.headers = {
            'Connection': 'close',
            'User-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; '
                          '+http://www.baidu.com/search/spider.html) '
        }
        if headers:
            self.headers.update(headers)

    def open(self, url, data=None) -> BinaryIO:
        req = Request(url, headers=self.headers)
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
