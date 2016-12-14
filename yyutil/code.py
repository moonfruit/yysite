# -*- coding: utf-8 -*-
import importlib

from collections import Mapping


def attr(string: str):
    if '.' in string:
        index = string.rindex('.')
        module = string[:index]
        name = string[index + 1:]
        module = importlib.import_module(module)
    else:
        module = globals()
        name = string

    return module[name] if isinstance(module, Mapping) else getattr(module, name)


def build(clazz, **kwargs):
    if isinstance(clazz, Mapping):
        data = dict(clazz)
        data.update(kwargs)
        clazz = data.pop('()')

    else:
        data = kwargs

    if not callable(clazz):
        clazz = attr(clazz)

    return clazz(**data)
