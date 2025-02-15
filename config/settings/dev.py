from .docker import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

AUTH_PASSWORD_VALIDATORS = []

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: True
}

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_URL = "http://localhost:8000"
