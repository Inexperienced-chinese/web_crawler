from urllib.parse import urlparse

import tldextract


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
