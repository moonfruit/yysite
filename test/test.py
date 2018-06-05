# -*- coding: utf-8 -*-
import logging
import sys

from yyfeed.fetcher import *

logger = logging.getLogger(__name__)


def test_fetcher(fetcher):
    count = 0
    for i, item in enumerate(fetcher.fetch()):
        logger.info(' -------- [%d] ------[[', i)
        logger.info(item)
        logger.info(']]------ [%d] --------', i)
        count += 1
    logger.info('-------- total[%d] --------', count)


def main():
    # test_fetcher(IYingDiFetcher(size=1))
    # test_fetcher(JandanFetcher(browser='baiduspider'))
    # test_fetcher(IAppsFetcher())
    # test_fetcher(SmzdmFetcher())
    test_fetcher(TtrssFetcher())
    # test_fetcher(RosiyyFetcher())
    pass


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger('PIL.Image').setLevel(logging.WARNING)
    main()
