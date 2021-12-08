from __future__ import absolute_import

import logging
import os

from celery import Celery

from hangroo import settings

logger = logging.getLogger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangroo.settings')

app = Celery('hangroo')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(name="good_morning_task")
def good_morning_task():
    logger.info("I am here good_morning_message")
    

