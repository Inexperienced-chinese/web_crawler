import datetime
import os.path
import time
import warnings
from datetime import datetime

from urllib.request import urlopen

from setup import CommonSetup
from url_utils import UrlUtils, HeadRequest


def build_path_to_robot(domain):
    curr_path = os.path.join(CommonSetup.BASE_FOLDER, domain)
    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)
    return os.path.join(curr_path, 'robots.txt')


class Downloader:
    @staticmethod
    def download_robot(domain: str):
        with open(build_path_to_robot(domain), 'w') as f:
            try:
                robots = urlopen(f"https://{domain}/robots.txt")
                f.write(robots.read().decode('cp1251'))
            except:
                warnings.warn(f"Bad robots.txt on {domain}")

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
        try:
            html = urlopen(url)
            path = UrlUtils.build_path_to_page(url)

            with open(path, 'w') as f:
                f.write(html.read().decode('cp1251'))
            return path
        except:
            warnings.warn("Something goes wrong while downloading")

    @staticmethod
    def update(url):
        last_update = Downloader.get_last_update_time(url)
        if last_update is None:
            time.sleep(0.5)
            return Downloader.download(url)

        timedelta = datetime.now() - last_update
        if timedelta > CommonSetup.UPDATE_TIMEDELTA:
            time.sleep(0.5)
            return Downloader.download(url)
