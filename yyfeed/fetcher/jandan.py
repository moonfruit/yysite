# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import re
from time import time
from typing import Iterable

# noinspection PyProtectedMember
from bs4 import SoupStrainer

from .base import Fetcher, Item

logger = logging.getLogger(__name__)


class JandanFetcher(Fetcher):
    URL = 'http://jandan.net/ooxx'
    FILTER = SoupStrainer('ol', 'commentlist')

    def __init__(self, count=5):
        super().__init__()
        self.count = count
        self.fetcher.browser = 'random'
        self.fetcher.every_time = True

    def fetch(self, count=None) -> Iterable[Item]:
        if count is None:
            count = self.count

        current = 1
        key = None
        for i in range(count):
            if i == 0:
                soup = self.fetcher.soup(self.URL)
                key = self.get_key(soup)
                logger.debug("Get key [%s]", key)

                current = int(soup.find('span', 'current-comment-page').text[1: -1])
                ol = soup.find(self.FILTER)
                for item in self.generate(ol, key):
                    yield item

            else:
                current -= 1
                for item in self.fetch_page(current, key):
                    yield item

    def fetch_page(self, page, key) -> Iterable[Item]:
        if not key:
            raise RuntimeError("No key")

        url = '%s/page-%d' % (self.URL, page)
        ol = self.fetcher.soup(url, parse_only=self.FILTER)
        return self.generate(ol, key)

    def get_key(self, soup) -> str:
        scripts = soup.find('head').find_all('script')
        key_url = None
        for script in scripts:
            src = script.get('src')
            if src and re.match(r'//cdn.jandan.net/static/min/\w+\.\d+\.js', src, re.ASCII):
                key_url = src
        if not key_url:
            raise RuntimeError("Cannot get key url")
        key_url = normalize(key_url)

        key = self.cache.get(key_url)
        if key is not None:
            return key

        js = self.fetcher.fetch(key_url)
        match = re.search(r'jandan_load_img\(.*\){.*f_\w+\(.*?"(.*?)"\).*}', js, re.ASCII)
        key = None
        if match:
            key = match.group(1)
        if not key:
            raise RuntimeError("Cannot get key from [%s]" % key_url)

        self.cache.set(key_url, key)
        return key

    @staticmethod
    def generate(ol, key) -> Iterable[Item]:
        for item in ol.find_all('li'):
            if not item.get('id'):
                continue

            text = item.find('div', 'text')
            a = text.find('span', 'righttext').a

            imgs = []
            for img in text.find_all('span', 'img-hash'):
                src = normalize(decode(img.text, key))
                imgs.append('<div><img src="%s"/></div>' % src)

            if imgs:
                yield Item(a.text, a.text, None, normalize(a['href']), ''.join(imgs))


def normalize(url):
    if url.startswith('//'):
        url = "http:" + url
    return url


def md5(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.md5(text).hexdigest()


def base64decode(text):
    mod = len(text) % 4
    if mod != 0:
        text += '=' * (4 - mod)
    return base64.b64decode(text)


def decode(cipher, key):
    if not key:
        key = ''
    key = md5(key)
    key_head = md5(key[:16])
    key_tail = md5(key[16:])

    cipher_head = cipher[:4]
    secret = key_head + md5(key_head + cipher_head)

    cipher_tail = cipher[4:]
    cipher_tail = base64decode(cipher_tail)

    array = list(range(256))
    array2 = [ord(secret[i % len(secret)]) for i in range(256)]

    index = 0
    for i in range(256):
        index = (index + array[i] + array2[i]) % 256
        array[i], array[index] = array[index], array[i]

    result = ''
    index = index2 = 0
    for i in range(len(cipher_tail)):
        index = (index + 1) % 256
        index2 = (index2 + array[index]) % 256
        array[index], array[index2] = array[index2], array[index]
        result += chr(cipher_tail[i] ^ (array[(array[index] + array[index2]) % 256]))

    timestamp = int(result[:10])
    expected = result[10:26]
    result = result[26:]
    actual = md5(result + key_tail)[:16]

    if timestamp != 0 and timestamp - time() <= 0:
        raise RuntimeError("Invalid timestamp [%s]" % timestamp)

    if expected != actual:
        raise RuntimeError("Not match mac")

    result = re.sub(r'(//\w+\.sinaimg\.cn/)(\w+)(/.+\.(gif|jpg|jpeg))', '\\1large\\3', result)

    return result
