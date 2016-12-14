# -*- coding: utf-8 -*-
try:
    import pylibmc as memcache
except ImportError:
    import memcache

from .base import Cache


class MemCache(Cache):
    def __init__(self, servers=None, **kargs):
        if servers is None:
            self.cache = memcache.Client(**kargs)
        else:
            self.cache = memcache.Client(servers, **kargs)

    def set(self, key, value, timeout=0):
        self.cache.set(key, value, time=timeout)

    def get(self, key, default=None):
        value = self.cache.get(key)
        return default if value is None else value

    def get_stats(self):
        return self.cache.get_stats()
