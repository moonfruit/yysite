# -*- coding: utf-8 -*-
from datetime import datetime

try:
    # noinspection PyUnresolvedReferences
    from django.core.exceptions import ImproperlyConfigured
    # noinspection PyUnresolvedReferences
    from django.utils import timezone


    def now():
        try:
            return timezone.now()
        except ImproperlyConfigured:
            return datetime.now()


    def fromtimestamp(timestamp):
        try:
            tzinfo = timezone.get_current_timezone()
        except ImproperlyConfigured:
            tzinfo = None
        return datetime.fromtimestamp(timestamp, tz=tzinfo)

except ImportError:
    def now():
        return datetime.now()


    def fromtimestamp(timestamp):
        return datetime.fromtimestamp(timestamp)
