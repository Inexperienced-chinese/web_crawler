import unittest
import urllib.request
from downloader import Downloader
from url_utils import UrlUtils


class Test(unittest.TestCase):
    def test_last_update(self):
        print(Downloader.get_last_update_time('https://stackoverflow.com'))

    def test_download(self):
        print(Downloader.download('http://python.org/'))

    def test_update(self):
        for i in range(5):
            print(Downloader.update('https://stackoverflow.com/'))

    def test_get_domain(self):
        print(UrlUtils.get_domain_with_lvl("https://try.stackoverflow.co", lvl=2))

    def test_download_robot(self):
        Downloader.download_robot("vk.com")

    def test_many_download(self):
        Downloader.download_robot("stackoverflow.com")

        Downloader.update("https://stackoverflow.com")
        Downloader.update("https://stackoverflow.com/questions")
        Downloader.update("https://stackoverflow.com/tags")
        Downloader.update("http://python.org")
