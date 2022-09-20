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


def build_path_to_page(domain, num):
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

    @staticmethod
    def url_index_load(domain):
        try:
            path = os.path.join(CommonSetup.BASE_FOLDER, domain, CommonSetup.URL_INDEX_FILE)
            with open(path, 'r') as f:
                Downloader.URL_INDEX = json.load(f)
        except FileNotFoundError:
            warnings.warn("No url_index file")

    @staticmethod
    def url_index_dump(domain):
        with open(os.path.join(CommonSetup.BASE_FOLDER, domain, CommonSetup.URL_INDEX_FILE), 'w') as f:
            json.dump(Downloader.URL_INDEX, f)

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

    @staticmethod
    def download(url):
        if url not in Downloader.URL_INDEX:
            Downloader.URL_INDEX[url] = len(Downloader.URL_INDEX) + 1

        domain = urlparse(url).netloc
        try:
            html = urlopen(url).read().decode('cp1251')
            path = Path(build_path_to_page(domain, Downloader.URL_INDEX[url]))

            with open(path, 'w') as f:
                f.write(html)

            Downloader.url_index_dump(domain)
            return path
        except:
            warnings.warn("Something goes wrong while downloading")

    @staticmethod
    def update(url):
        domain = urlparse(url).netloc
        Downloader.url_index_load(domain)

        last_update = Downloader.get_last_update_time(url)
        if url not in Downloader.URL_INDEX or last_update is None:
            return Downloader.download(url)

        timedelta = datetime.now() - last_update
        if timedelta > CommonSetup.UPDATE_TIMEDELTA:
            return Downloader.download(url)
