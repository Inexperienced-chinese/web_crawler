from urllib.parse import urlparse

from html_parser import HtmlParser
from url_utils import UrlUtils
import unittest


class Test(unittest.TestCase):
    def test_building_path(self):
        print(UrlUtils.build_path_to_page(
            "https://ulearn.me/course/BasicProgramming2/Listy_i_indeksatsiya_ff0b5f9b-eb8c-432d-8bab-4bfa9718469a"))
