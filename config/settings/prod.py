from .docker import *

DEBUG = False

SITE_URL = "http://13.53.119.20:8080"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
