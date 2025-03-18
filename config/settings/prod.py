from .docker import *

DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_URL = "https://lms-server-e5b12b7c980b.herokuapp.com/"

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
