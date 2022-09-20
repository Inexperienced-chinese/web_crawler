from html_parser import HtmlParser
from common_setup import CommonSetup
from downloader import Downloader
from url_utils import UrlUtils

class Crawler:

    @staticmethod
    def update():
        for domain in CommonSetup.ALLOWED_DOMAINS:
            Crawler.parse_domain(domain)

    @staticmethod
    def parse_domain(domain):
        passed_urls = set()
        url_html_path = {}
        curr_html_path = Downloader.update(domain)
        if curr_html_path is None:
            return
        url_stack = [domain]
        while len(url_stack) != 0:
            curr_url = url_stack.pop(url_stack[-1])
            curr_html_path = Downloader.update(curr_url)
            if curr_html_path is None:
                continue
            for url in HtmlParser.get_urls_from_html(curr_html_path):
                url = UrlUtils.crop_url_params(url)
                # TODO: Реализовать проверку на соответствие robot.txt
                if url not in passed_urls:
                    url_stack.append(url)
            passed_urls.add(curr_url)