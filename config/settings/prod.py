from .docker import *

DEBUG = False

SITE_URL = "http://16.171.11.192:8080"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
