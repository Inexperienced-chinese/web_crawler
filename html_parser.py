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
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = [img['src'] for img in img_tags]

        for image_url in image_urls:

            if 'http' not in image_url:
                image_url = '{}{}'.format(url, image_url)

            if UrlUtils.get_image_size(image_url) > max_bytes:
                continue

            with open(UrlUtils.build_path_to_image(image_url), "wb") as image_file:
                response = urlopen(image_url)
                image_file.write(response.read())
