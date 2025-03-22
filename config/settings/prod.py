from .docker import *

DEBUG = False

SITE_URL = "http://16.16.207.86:8080"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
