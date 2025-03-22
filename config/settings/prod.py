from .docker import *

DEBUG = False

SITE_URL = "http://3.120.187.32:8080"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
