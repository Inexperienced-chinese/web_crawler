import datetime


class CommonSetup:
    BASE_FOLDER = 'database/'
    URL_INDEX_FILE = 'url_index.json'
    DATE_TIME_PATTERN = '%a, %d %b %Y %H:%M:%S %Z'
    UPDATE_TIMEDELTA = datetime.time(0, 30, 0, 0)
    ALLOWED_DOMAINS = ['https://stackoverflow.com/']
