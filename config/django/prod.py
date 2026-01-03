from .base import *

CSRF_TRUSTED_ORIGINS = [
    os.environ.get("CSRF_TRUSTED_ORIGIN"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST"),
        "PORT": os.environ.get("PGPORT"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

RQ_QUEUES = {
    "default": {
        "HOST": env("REDISHOST"),
        "PORT": env.int("REDISPORT"),
        "DB": env.int("REDISDB"),
        "PASSWORD": env("REDISPASSWORD"),
        "DEFAULT_TIMEOUT": env.int("RQ_DEFAULT_TIMEOUT"),
    },
}