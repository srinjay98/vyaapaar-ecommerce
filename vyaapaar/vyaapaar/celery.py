import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'vyaapaar.settings'
)

app = Celery('vyaapaar')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks()