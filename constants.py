import datetime


class Constans:
    BASE_FOLDER = 'database/'
    META_FILE = 'meta.json'
    URL_INDEX_FILE = 'url_index.json'
    SITE_DATE_TIME_PATTERN = '%a, %d %b %Y %H:%M:%S %Z'
    LOCAL_DATE_TIME_PATTERN = "%Y-%m-%d %H:%M:%S.%f"
    UPDATE_TIMEDELTA = datetime.time(0, 30, 0, 0)
    ALLOWED_DOMAINS = ['python.org/', 'stackoverflow.com/']
    THREADS_IN_QUEUE = 5