# -*- coding: utf-8 -*-
from yyfeed.fetcher import IYingDiFetcher, JandanFetcher


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


def main():
    jandan()


if __name__ == '__main__':
    main()
