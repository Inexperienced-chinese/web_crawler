import tldextract


class UrlUtils:
    @staticmethod
    def get_url_domain(url):
        ext = tldextract.extract(url)
        return ext.domain

    @staticmethod
    def filter_urls_by_domains(urls, domains):
        for url in urls:
            if UrlUtils.get_url_domain(url) in domains:
                yield url

    @staticmethod
    def crop_url_params(url):
        # TODO: Сделать метод для удаления параметров из url
        return url
