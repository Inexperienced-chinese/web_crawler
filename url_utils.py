import os.path
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urlparse
from urllib.request import urlopen

from constants import Constans
import re


def build_path_by_url(url):
    p = urlparse(url)
    path_list = p.path.split('/')[1:]
    curr_path = os.path.join(Constans.BASE_FOLDER, p.netloc)
    if not os.path.isdir(curr_path):
        os.mkdir(curr_path)

    for folder in path_list[:-1]:
        curr_path = os.path.join(curr_path, folder)
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

    return curr_path, path_list[-1]


class UrlUtils:
    @staticmethod
    def get_domain_with_lvl(url: str, lvl=0):
        full_domain = urlparse(url).netloc
        splited_domain = full_domain.split('.')
        lvl_domain = '.'.join(splited_domain[-lvl:])

        return lvl_domain

    @staticmethod
    def get_format_url(url, page_url):
        if url is None or len(url) == 0 or 'javascript' in url or '#' in url:
            return None

        if '?' in url:
            url = url[:url.find('?')]
        if len(url) == 0:
            return None
        if url[-1] == '/':
            url = url[:-1]
        if len(url) == 0:
            return None
        if url[0] == '/':
            url = page_url + url[1:]
        return url

    @staticmethod
    def build_path_to_page(url):
        path, name = build_path_by_url(url)
        return os.path.join(path, f"{name}.html")

    @staticmethod
    def get_image_size(url):
        headers_response = urlopen(HeadRequest(url))
        content_length = int(dict(headers_response.info()).get('Content-Length'))
        return content_length

    @staticmethod
    def build_path_to_image(image_url):
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image_url)
        if filename is None:
            return None
        path, name = build_path_by_url(image_url)
        return os.path.join(path, filename.group(1))

    @staticmethod
    def build_path_to_meta(url):
        path, name = build_path_by_url(url)
        return os.path.join(path, Constans.META_FILE)

    @staticmethod
    def build_path_to_url_index(domain):
        return os.path.join(os.path.join(Constans.BASE_FOLDER, domain), Constans.URL_INDEX_FILE)


class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"
