from .docker import *


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda x: False,
    # 'IS_RUNNING_TESTS': False
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_URL = "http://localhost:8080"