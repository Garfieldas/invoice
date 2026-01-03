from .base import *

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': env('RQ_DEFAULT_HOST'),
        'PORT': env.int('RQ_DEFAULT_PORT'),
        'DB': env.int('RQ_DEFAULT_DB'),
        'DEFAULT_TIMEOUT': env.int('RQ_DEFAULT_TIMEOUT'),
    },
    'low': {
        'HOST': env('RQ_LOW_HOST'),
        'PORT': env.int('RQ_LOW_PORT'),
        'DB': env.int('RQ_LOW_DB'),
        'DEFAULT_TIMEOUT': env.int('RQ_LOW_TIMEOUT'),
    },
}