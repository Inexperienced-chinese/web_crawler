import unittest
import urllib.request


from downloader import Downloader
from url_utils import UrlUtils


class Test(unittest.TestCase):
    def test_last_update(self):
        print(Downloader.get_last_update_time('https://stackoverflow.com'))

    def test_download(self):
        print(Downloader.download('https://stackoverflow.com/users'))

    def test_update(self):
        print(Downloader.update('https://stackoverflow.com'))

    def test_get_domain(self):
        print(UrlUtils.get_domain_with_lvl("https://try.stackoverflow.co"))

    def test_download_robot(self):
        Downloader.download_robot("vk.com")
