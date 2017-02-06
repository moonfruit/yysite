# -*- coding: utf-8 -*-

import logging

from yyfeed.fetcher import *


def test_fetcher(fetcher):
    count = 0
    for i, item in enumerate(fetcher.fetch()):
        print('-------- [%d] --------' % i)
        print(item)
        count += 1
    print('-------- total[%d] --------' % count)


def main():
    # test_fetcher(IYingDiFetcher(size=1))
    # test_fetcher(JandanFetcher())
    # test_fetcher(IAppsFetcher())
    test_fetcher(SmzdmFetcher())
    # test_fetcher(TtrssFetcher())
    # test_fetcher(RosiyyFetcher())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
