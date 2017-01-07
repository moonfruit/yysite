# -*- coding: utf-8 -*-
from yyfeed.fetcher import IAppsFetcher, IYingDiFetcher, JandanFetcher


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


def main():
    iapps()


if __name__ == '__main__':
    main()
