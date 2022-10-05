import datetime
import os.path
import time
import warnings
from datetime import datetime
from urllib.request import urlopen
from constants import Constans
from url_utils import UrlUtils, HeadRequest
import json


def build_path_to_robot(domain):
    curr_path = os.path.join(Constans.BASE_FOLDER, domain)
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
            converted = datetime.strptime(last_modified, Constans.SITE_DATE_TIME_PATTERN)
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
        res = None
        meta = Meta(url)
        last_modified = Downloader.get_last_update_time(url)
        last_update = meta.meta_dict["last_update"]
        if last_update is None \
                or last_modified is None \
                or last_modified - last_update > Constans.UPDATE_TIMEDELTA:
            time.sleep(0.5)
            res = Downloader.download(url)

        meta.meta_dict["last_update"] = datetime.now()
        meta.dump()

        return res


class Meta:
    meta_dict = None
    deserializers = {"last_update": lambda x: datetime.strptime(x, Constans.LOCAL_DATE_TIME_PATTERN)}

    def __init__(self, url):
        self.path = UrlUtils.build_path_to_meta(url)
        self.load()

    def dump(self):
        serialized_dict = dict()
        for k, v in self.meta_dict.items():
            serialized_dict[k] = str(v)

        with open(self.path, 'w') as f:
            json.dump(serialized_dict, f)

    def load(self):
        try:
            open(self.path, 'a').close()  # костыль, питон иди нахер
            with open(self.path, 'r') as f:
                self.meta_dict = json.load(f)

                # if self.meta_dict == {}:
                #     self.create_meta()
                #     return

                for k, v in self.meta_dict.items():
                    self.meta_dict[k] = self.deserializers[k](v)
        except:
            warnings.warn("Creating meta...")
            self.create_meta()

    def create_meta(self):
        self.meta_dict = dict()
        self.meta_dict["last_update"] = None

    def update(self, **kwargs):
        for k, v in kwargs:
            self.meta_dict[k] = v

    def __str__(self):
        return f"path: {self.path}; meta :{self.meta_dict}"
