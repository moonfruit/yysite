# -*- coding: utf-8 -*-

import logging

from yyfeed.fetcher import *


def iyingdi():
    fetcher = IYingDiFetcher(size=1)
    print(fetcher.url())
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def jandan():
    fetcher = JandanFetcher()
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def iapps():
    fetcher = IAppsFetcher()
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def smzdm():
    fetcher = SmzdmFetcher()
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def ttrss():
    fetcher = TtrssFetcher()
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def rosiyy():
    fetcher = RosiyyFetcher()
    items = fetcher.fetch()
    print(len(items))
    for item in items:
        print(item)


def main():
    rosiyy()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
