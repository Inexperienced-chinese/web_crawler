import datetime

from celery.schedules import crontab


class CommonSetup:
    BASE_FOLDER = 'database/'
    URL_INDEX_FILE = 'url_index.json'
    DATE_TIME_PATTERN = '%a, %d %b %Y %H:%M:%S %Z'
    UPDATE_TIMEDELTA = datetime.time(0, 30, 0, 0)
    ALLOWED_DOMAINS = ['python.org', 'stackoverflow.com']

    BEATS_TASKS = {
        'update-2m': {
            'task': "tasks.tasks.add",
            'schedule': crontab(minute='*/2'),
            'args': (1, 2)
        }
    }


CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'  # 'django-db'

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SOFT_TIME_LIMIT = '20'  # seconds
CELERY_TASK_TIME_LIMIT = '30'  # seconds
CELERY_TASK_MAX_RETRIES = '3'
