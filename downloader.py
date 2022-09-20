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
from url_utils import UrlUtils


def build_path_to_page(domain, num):
    curr_path = os.path.join(CommonSetup.BASE_FOLDER, domain)
    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)
        curr_path = os.path.join(curr_path, "pages")

    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)

    return os.path.join(CommonSetup.BASE_FOLDER, domain, "pages", f"{num}.html")


def build_path_to_robot(domain):
    curr_path = os.path.join(CommonSetup.BASE_FOLDER, domain)
    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)
    return os.path.join(curr_path, 'robots.txt')


class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"


class Downloader:
    URL_INDEX = dict()

    @staticmethod
    def download_robot(domain: str):
        with open(build_path_to_robot(domain), 'w') as f:
            try:
                robots = urlopen(f"https://{domain}/robots.txt")
                f.write(robots.read().decode('cp1251'))
            except:
                warnings.warn(f"Bad robots.txt on {domain}")

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
        last_modified = None
        try:
            headers_response = urlopen(HeadRequest(url))
            last_modified = dict(headers_response.info()).get('last-modified')
        except:
            warnings.warn(f"Can't download page: {url}")

        if last_modified is None:
            return None

        converted = None
        try:
            converted = datetime.strptime(last_modified, CommonSetup.DATE_TIME_PATTERN)
        except ValueError:
            warnings.warn("Wrong datetime format")
        return converted

    @staticmethod
    def download(url):
        if url not in Downloader.URL_INDEX:
            Downloader.URL_INDEX[url] = len(Downloader.URL_INDEX) + 1

        domain = UrlUtils.get_domain_with_lvl(url)
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
        domain = UrlUtils.get_domain_with_lvl(url)
        Downloader.url_index_load(domain)

        last_update = Downloader.get_last_update_time(url)
        if url not in Downloader.URL_INDEX or last_update is None:
            return Downloader.download(url)

        timedelta = datetime.now() - last_update
        if timedelta > CommonSetup.UPDATE_TIMEDELTA:
            return Downloader.download(url)
