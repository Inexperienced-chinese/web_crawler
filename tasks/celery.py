from __future__ import absolute_import
from celery import Celery

from setup import CommonSetup

app = Celery('web_crawler', include=['tasks.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('setup', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = CommonSetup.BEATS_TASKS
