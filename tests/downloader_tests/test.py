import unittest
import urllib.request


from downloader import Downloader


class Test(unittest.TestCase):
    def test_last_update(self):
        print(Downloader.get_last_update_time("https://stackoverflow.com"))

    def test_download(self):
        print(Downloader.download("https://stackoverflow.com"))
