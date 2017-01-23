# -*- coding: utf-8 -*-
import importlib
import json

from collections import Mapping
from json import JSONDecodeError
from typing import Text


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
    if isinstance(clazz, Text):
        try:
            clazz = json.loads(clazz)
        except JSONDecodeError:
            pass

    if isinstance(clazz, Mapping):
        data = dict(clazz)
        data.update(kwargs)
        clazz = data.pop('()')

    else:
        data = kwargs

    if not callable(clazz):
        clazz = attr(clazz)

    return clazz(**data)
