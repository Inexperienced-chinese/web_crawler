import datetime
import json
import os.path
import urllib.request
import warnings
from datetime import datetime

from urllib.parse import urlparse
from urllib.request import urlopen

from setup import CommonSetup
from pathlib import Path


def build_path(domain, num):
    curr_path = os.path.join(CommonSetup.BASE_FOLDER, domain)
    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)
        curr_path = os.path.join(curr_path, "pages")

    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)

    return os.path.join(CommonSetup.BASE_FOLDER, domain, "pages", f"{num}.html")


class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"


class Downloader:
    URL_INDEX = dict()

    @classmethod
    def url_index_load(cls):
        try:
            cls.URL_INDEX = json.load(CommonSetup.URL_INDEX_FILE)
        except FileNotFoundError:
            warnings.warn("No url_index file")

    @classmethod
    def url_index_dump(cls, domain):
        with open(os.path.join(CommonSetup.BASE_FOLDER, domain, CommonSetup.URL_INDEX_FILE), 'w') as f:
            json.dump(cls.URL_INDEX, f)

    @staticmethod
    def get_last_update_time(url):
        headers_response = urlopen(HeadRequest(url))
        last_modified = dict(headers_response.info()).get('last-modified')

        converted = None

        if last_modified is None:
            return None

        try:
            converted = datetime.strptime(last_modified, CommonSetup.DATE_TIME_PATTERN)
        except ValueError:
            warnings.warn("Wrong datetime format")
        return converted

    @classmethod
    def download(cls, url):
        if url not in cls.URL_INDEX:
            cls.URL_INDEX[url] = len(cls.URL_INDEX) + 1

        domain = urlparse(url).netloc
        html = urlopen(url).read().decode('utf-8')
        path = Path(build_path(domain, cls.URL_INDEX[url]))
        with open(path, 'w') as f:
            f.write(html)

        cls.url_index_dump(domain)
        return path

    @classmethod
    def update(cls, url):
        last_update = cls.get_last_update_time(url)
        if url not in cls.URL_INDEX or last_update is None:
            return cls.download(url)

        timedelta = datetime.now() - last_update
        if timedelta > CommonSetup.UPDATE_TIMEDELTA:
            return cls.download(url)
