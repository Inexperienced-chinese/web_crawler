import urllib.robotparser
from html_parser import HtmlParser

rp = urllib.robotparser.RobotFileParser()
with open('robots.txt') as rp_file:
    rp.parse(rp_file.readlines())
rrate = rp.request_rate("*")
urls = HtmlParser.get_urls_from_html('1.html', 'https://stackoverflow.com/')

for url in sorted(urls):
    print(url, rp.can_fetch('*', url))