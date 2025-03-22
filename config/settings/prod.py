from .docker import *

DEBUG = False

SITE_URL = "http://13.60.78.222:8080"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
