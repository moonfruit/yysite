# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
from .settings import *

ETC_DIR = os.path.join(BASE_DIR, 'etc')

# Django
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1', '.moonfruit.top']

with open(os.path.join(ETC_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

STATIC_ROOT = os.path.join(VAR_DIR, 'static')
MEDIA_ROOT = os.path.join(VAR_DIR, 'media')

os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

# Log
LOGGING.update({
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
})

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/run/memcached.sock',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# noinspection SpellCheckingInspection
EMAIL_HOST_PASSWORD = ''

# YYFeed
YYFEED_CACHE = {
    '()': 'yyutil.cache.MemCache',
    'servers': ['/var/run/memcached.sock'],
}
