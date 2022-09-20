from bs4 import BeautifulSoup
from url_utils import UrlUtils


class HtmlParser:
    @staticmethod
    def get_urls_from_html(html_file_path, page_url):
        urls = set()
        with open(html_file_path, 'r', encoding='cp1251') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
            quotes = soup.find_all('a')
            for quote in quotes:
                url = UrlUtils.get_format_url(quote.get('href'), page_url)
                if url is not None:
                    urls.add(url)
        return sorted(list(urls))
