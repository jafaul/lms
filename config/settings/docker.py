from config.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

CELERY_BROKER_URL = 'redis://redis/0'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
