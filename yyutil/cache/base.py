# -*- coding: utf-8 -*-
import os
import pickle

from abc import ABCMeta, abstractmethod


class Cache(metaclass=ABCMeta):
    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    @abstractmethod
    def get(self, key, default=None):
        pass

    @abstractmethod
    def set(self, key, value, timeout=0):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class DummyCache(Cache):
    def get(self, key, default=None):
        return default

    def set(self, key, value, timeout=0):
        pass

    def get_stats(self):
        return True


class FileCache(Cache):
    def __init__(self, filename=".cache"):
        self.filename = os.path.abspath(filename)
        self.cache = {}

        try:
            with open(self.filename, 'rb') as stream:
                self.cache.update(pickle.load(stream))
        except FileNotFoundError:
            pass

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value, timeout=0):
        self.cache[key] = value
        with open(self.filename, "wb") as stream:
            pickle.dump(self.cache, stream)

    def get_stats(self):
        return self.filename
