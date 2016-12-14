# -*- coding: utf-8 -*-
from yyfeed.fetcher.iyingdi import IYingDiFetcher


def main():
    fetcher = IYingDiFetcher(size=1)
    print(fetcher.url())
    for item in fetcher.fetch():
        print(item)


if __name__ == '__main__':
    main()
