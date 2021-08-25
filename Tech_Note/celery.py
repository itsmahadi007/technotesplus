from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tech_Note.settings')

app = Celery('Tech_Note')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

from django.apps import apps

# app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
# Load task modules from all registered Django apps.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()
# app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-2-hour': {
        'task': 'send_notification',
        'schedule': crontab(minute='*/2')
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {self.request!r}')
