import requests
from bs4 import BeautifulSoup


class HtmlParser:
    @staticmethod
    def get_urls_from_html(html_file_path):
        urls = []
        with open(html_file_path, 'r', encoding='utf8') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
            quotes = soup.find_all('a')
            for quote in quotes:
                urls.append(quote.get('href'))

        return urls
