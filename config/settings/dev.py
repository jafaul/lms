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
    "SHOW_TOOLBAR_CALLBACK": lambda x: True,
}

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_URL = "http://localhost:8080"


import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    print("TEST")

    DEBUG_TOOLBAR_CONFIG.update({
        'IS_RUNNING_TESTS': False
    })

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #     }
    # }

    print(DATABASES)