from urllib.parse import urlparse

from html_parser import HtmlParser
from url_utils import UrlUtils
import unittest


class Test(unittest.TestCase):
    def test_get_utils(self):
        start_page_path = 'C:\\Users\\lovyg\\OneDrive\\Документы\\GitHub\\web_crawler\\database\\stackoverflow.com\\pages\\1.html'
        urls = HtmlParser.get_urls_from_html(start_page_path, 'https://stackoverflow.com')
        for url in urls:
            print(url, urlparse(url).netloc)

    def test_get_images(self):
        HtmlParser.get_images('https://www.python.org/')
