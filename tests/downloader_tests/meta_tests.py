import os
from datetime import datetime
import unittest
import urllib.request
import time

from downloader import Downloader, Meta
from url_utils import UrlUtils, HeadRequest
from setup import CommonSetup
from urllib.request import urlopen


class Test(unittest.TestCase):

    def test_meta_init(self):
        meta = Meta("http://python.org/")
        self.assertTrue(meta.meta_dict is not None )
        self.assertTrue(meta.path is not None)

    def test_meta_dump_and_load(self):
        pattern = "%Y-%m-%d %H:%M:%S.%f"

        url = "http://python.org/"
        meta = Meta(url)
        time_now = datetime.now()
        meta.meta_dict["last_update"] = time_now
        meta.dump()
        time.sleep(5)
        meta.load()

        self.assertEqual(datetime.strptime(meta.meta_dict["last_update"], pattern), time_now)
