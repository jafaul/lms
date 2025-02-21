import os

from celery import Celery
from celery.schedules import crontab

from config.settings.base import REDIS_ADDR

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('lms-proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    broker_url=f'redis://{REDIS_ADDR}/0',
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=5,
    broker_connection_retry=True,
    broker_connection_retry_delay=2.0
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-mail-every-day-at-8": {
        'task': 'apps.management.tasks.send_course_starts_tomorrow_email',
        'schedule': crontab(minute='00', hour='08'),
        # 'args': (),
    },
    "clean-non-usable-test-users": {
        'task': 'apps.authentication.tasks.clean_usable_users',
        'schedule': crontab(minute="38"),
    }
}