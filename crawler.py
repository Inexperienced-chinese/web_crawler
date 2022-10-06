from html_parser import HtmlParser
from downloader import Downloader, build_path_to_robot, Meta
from url_utils import UrlUtils
import urllib.robotparser
import threading


class Crawler:
    working_threads = queue.Queue(maxsize=CommonSetup.THREADS_IN_QUEUE)

    @staticmethod
    def make_url_thread(url, domain, stack, rp):
        t = threading.Thread(target=Crawler.parse_url, args=(url, domain, stack, rp))
        t.setName(url)
        return t

    @staticmethod
    def update(domains):
        for domain in domains:
            t = threading.Thread(target=Crawler.download_domain, args=(domain,))
            t.start()
            # Crawler.parse_domain(domain)

    @staticmethod
    def parse_domain(domain):
        domain_threads_stack = []

    @staticmethod
    def update_domain(domain):
        meta = Meta(f"https://{domain}")
        for url in meta.meta_dict["adjacent_urls"]:
            Downloader.update(url)

    @staticmethod
    def download_domain(domain):
        domain_threads_stack = []
        rp = urllib.robotparser.RobotFileParser()

        page_thread = Crawler.make_url_thread(f"https://{domain}", domain, domain_threads_stack, rp)
        domain_threads_stack.append(page_thread)

        Downloader.download_robot(domain)
        with open(build_path_to_robot(domain)) as robots_file:
            rp.parse(robots_file.readlines())

        while domain_threads_stack:
            new_thread = domain_threads_stack.pop()
            top_thread = None
            if not Crawler.working_threads.empty():
                top_thread = Crawler.working_threads.get()
            # while top_thread is not None and top_thread.is_alive():
            #     time.sleep(1)
            Crawler.working_threads.put(new_thread.start())
            time.sleep(5)
            # passed_urls.add(fulfilled_thread.name)
            # print(curr_url)

    @staticmethod
    def parse_url(curr_url, domain, stack, rp):
        print(f"Hello from thread:{curr_url}")

        HtmlParser.get_images(curr_url)

        curr_html_path = Downloader.update(curr_url)
        if curr_html_path is None:
            return

        a = HtmlParser.get_urls_from_html(curr_html_path, curr_url)
        for url in a:
            if rp.can_fetch('*', url) and \
                    UrlUtils.get_domain_with_lvl(f"https://{domain}", lvl=2) == UrlUtils.get_domain_with_lvl(url, lvl=2):
                stack.append(Crawler.make_url_thread(url, domain, stack, rp))
