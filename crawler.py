from html_parser import HtmlParser
from setup import CommonSetup
from downloader import Downloader, build_path_to_robot
from url_utils import UrlUtils
import urllib.robotparser
import threading


class Crawler:

    @staticmethod
    def update():
        for domain in CommonSetup.ALLOWED_DOMAINS:
            t = threading.Thread(target=Crawler.parse_domain, args=(domain,))
            t.start()
            #Crawler.parse_domain(domain)

    @staticmethod
    def parse_domain(domain):
        passed_urls = set()
        url_stack = [f"https://{domain}"]
        rp = urllib.robotparser.RobotFileParser()
        Downloader.download_robot(domain)
        with open(build_path_to_robot(domain)) as robots_file:
            rp.parse(robots_file.readlines())
        while len(url_stack) != 0:
            curr_url = url_stack.pop()
            passed_urls.add(curr_url)
            print(curr_url)
            curr_html_path = Downloader.update(curr_url)
            if curr_html_path is None:
                continue

            a = HtmlParser.get_urls_from_html(curr_html_path, curr_url)
            for url in a:
                if rp.can_fetch('*', url) and \
                        url not in passed_urls and \
                        UrlUtils.get_domain_with_lvl(f"https://{domain}") == UrlUtils.get_domain_with_lvl(url):
                    url_stack.append(url)