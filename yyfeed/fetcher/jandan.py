# -*- coding: utf-8 -*-
from base64 import b64decode
from hashlib import md5 as md5digest
from re import sub
from typing import Iterable

from bs4 import SoupStrainer

from .base import Fetcher, Item


class JandanFetcher(Fetcher):
    URL = 'http://jandan.net/ooxx'
    FILTER = SoupStrainer('ol', 'commentlist')

    def __init__(self, key='Aw9P1Fjfo2fJ0cigUoM094bJ4g8FPzop'):
        super().__init__()
        self.key = key

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

    def generate(self, ol) -> Iterable[Item]:
        for item in ol.find_all('li'):
            if not item.get('id'):
                continue

            text = item.find('div', 'text')
            a = text.find('span', 'righttext').a

            imgs = []
            for img in text.find_all('span', 'img-hash'):
                src = decode(img.text, self.key)
                imgs.append('<div><img src="%s"/></div>' % src)

            if imgs:
                yield Item(a.text, a.text, None, a['href'], ''.join(imgs))


def md5(text):
    if isinstance(text, str):
        text = text.encode()
    return md5digest(text).hexdigest()


def base64decode(text):
    mod = len(text) % 4
    if mod != 0:
        text += '=' * (4 - mod)
    return b64decode(text)


def decode(cipher, key):
    if not key:
        key = ''
    key = md5(key)
    key_head = md5(key[:16])

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

    results = []
    index = index2 = 0
    for i in range(len(cipher_tail)):
        index = (index + 1) % 256
        index2 = (index2 + array[index]) % 256
        array[index], array[index2] = array[index2], array[index]
        results.append(chr(cipher_tail[i] ^ (array[(array[index] + array[index2]) % 256])))

    results = ''.join(results)[26:]
    results = sub(r'(//\w+\.sinaimg\.cn/)(\w+)(/.+\.(gif|jpg|jpeg))', '\\1large\\3', results)
    if results.startswith('//'):
        results = "http:" + results

    return results
