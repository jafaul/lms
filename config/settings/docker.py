from config.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'testdb'),
        'USER': os.getenv('DB_USERNAME', 'testuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'example'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
print("DOCKER")
print(DATABASES)

# print(DATABASES)

# CELERY_BROKER_URL = 'redis://redis/0'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_ADDR}/1",
    }
}
