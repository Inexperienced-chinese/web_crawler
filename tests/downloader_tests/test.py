import unittest
import urllib.request


from downloader import Downloader, get_domain_with_lvl


class Test(unittest.TestCase):
    def test_last_update(self):
        print(Downloader.get_last_update_time('https://stackoverflow.com'))

    def test_download(self):
        print(Downloader.download('https://stackoverflow.com/users'))

    def test_update(self):
        print(Downloader.update('https://stackoverflow.com'))

    def test_get_domain(self):
        print(get_domain_with_lvl("https://try.stackoverflow.co"))
