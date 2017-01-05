# -*- coding: utf-8 -*-

import random
import string


def generate(length=50):
    return ''.join([random.SystemRandom().choice(
        string.ascii_letters + string.digits + string.punctuation) for i in range(length)])
