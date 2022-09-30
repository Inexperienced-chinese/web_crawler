import os.path
from urllib.parse import urlparse

import tldextract
from urllib.parse import urlparse

from setup import CommonSetup


class UrlUtils:
    @staticmethod
    def get_domain_with_lvl(url: str, lvl=2):
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

        p = urlparse(url)
        path_list = p.path.split('/')[1:]
        curr_path = os.path.join(CommonSetup.BASE_FOLDER, p.netloc)
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

        for folder in path_list[:-1]:
            curr_path = os.path.join(curr_path, folder)
            if not os.path.isdir(curr_path):
                os.mkdir(curr_path)

        return os.path.join(curr_path, f"{path_list[-1]}.html")
