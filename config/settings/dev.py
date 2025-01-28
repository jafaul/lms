from .docker import *

# DEBUG = 'True'

INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

AUTH_PASSWORD_VALIDATORS = []
