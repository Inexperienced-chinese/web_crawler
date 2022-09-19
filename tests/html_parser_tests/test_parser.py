from html_parser import HtmlParser
from url_utils import UrlUtils


if __name__ == '__main__':
    domains = {'kontur', 'github'}
    start_page_path = 'ulearn.me.html'
    urls = HtmlParser.get_urls_from_html(start_page_path)
    filtered_urls = UrlUtils.filter_urls_by_domains(urls, domains)
    for url in filtered_urls:
        print(url, UrlUtils.get_url_domain(url))