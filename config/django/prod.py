from .base import *

CSRF_TRUSTED_ORIGINS = [
    os.environ.get("CSRF_TRUSTED_ORIGIN"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

RQ_QUEUES = {
    "default": {
        "HOST": env("RQ_DEFAULT_HOST"),
        "PORT": env.int("RQ_DEFAULT_PORT"),
        "DB": env.int("RQ_DEFAULT_DB"),
        "DEFAULT_TIMEOUT": env.int("RQ_DEFAULT_TIMEOUT"),
    },
}