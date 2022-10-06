import warnings

from bs4 import BeautifulSoup
from url_utils import UrlUtils, HeadRequest
from urllib.request import urlopen
import re


class HtmlParser:
    @staticmethod
    def get_urls_from_html(html_file_path, page_url):
        urls = set()
        with open(html_file_path, 'r', encoding='cp1251') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
            quotes = soup.find_all('a')
            for quote in quotes:
                url = UrlUtils.get_format_url(quote.get('href'), page_url)
                if url is not None:
                    urls.add(url)
        return list(urls)

    @staticmethod
    def get_images(url, max_bytes=1000000):  # size in ...
        try:
            html = urlopen(url)
        except:
            warnings.warn("bad images")
            return
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = []
        for img in img_tags:
            try:
                image_urls.append(img['src'])
            except:
                continue

        for image_url in image_urls:

            if 'http' not in image_url:
                image_url = '{}{}'.format(url, image_url)

            if UrlUtils.get_image_size(image_url) > max_bytes:
                continue

            path = UrlUtils.build_path_to_image(image_url)
            if path is None:
                return

            with open(path, "wb") as image_file:
                response = urlopen(image_url)
                image_file.write(response.read())
