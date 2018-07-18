# -*- coding: utf-8 -*-
try:
    import pylibmc as memcache
except ImportError:
    import memcache

import logging

from .base import Cache

logger = logging.getLogger(__name__)


# noinspection PyBroadException
class MemCache(Cache):
    def __init__(self, servers, **kargs):
        self.cache = memcache.Client(servers, **kargs)

    def set(self, key, value, timeout=48 * 60 * 60):
        try:
            self.cache.set(key, value, time=timeout)
        except:
            logger.warning('Cannot cache key `%s`', key, exc_info=True)

    def get(self, key, default=None):
        value = None
        try:
            value = self.cache.get(key)
        except:
            logger.warning('Cannot retrieve cached key `%s`', key, exc_info=True)
        return default if value is None else value

    def get_stats(self):
        return self.cache.get_stats()
