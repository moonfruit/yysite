# -*- coding: utf-8 -*-
import json
from typing import BinaryIO, Union
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request
from urllib.request import build_opener

from bs4 import BeautifulSoup


class UrlFetcher:
    def __init__(self, headers=None):
        self.opener = build_opener(HTTPCookieProcessor())
        if headers:
            self.headers = headers
        else:
            self.headers = {
                'User-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; '
                              '+http://www.baidu.com/search/spider.html) '
            }

    def open(self, url, data=None) -> BinaryIO:
        req = Request(url, headers=self.headers)
        if data:
            req.data = urlencode(data)

        return self.opener.open(req)

    def fetch(self, url, data=None, encoding='utf-8') -> str:
        with self.open(url, data) as stream:
            return stream.read().decode(encoding)

    def json(self, url, data=None, encoding='utf-8') -> Union[dict, list]:
        return json.loads(self.fetch(url, data, encoding))

    def soup(self, url, data=None, **kwargs) -> BeautifulSoup:
        with self.open(url, data) as stream:
            return BeautifulSoup(stream, 'lxml', **kwargs)
