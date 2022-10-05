from downloader import Meta
from url_utils import UrlUtils


class GraphDrawer:

    def __init__(self, domain):
        self.domain = UrlUtils.get_domain_with_lvl(f"https://{domain}")
        self.urls = Meta(f"https://{domain}").meta_dict["adjacent_urls"]
        self.fill_graph(self.urls)


    def fill_graph(self, urls):
        graph = {}
        for url in urls:
            split_url = url.split('/')
            for i in range(len(split_url) - 1):
                if split_url[i] not in graph:
                    graph[split_url[i]] = []
                graph[split_url[i]].append(split_url[i + 1])
        self.graph = graph


    def get_graph_view(self):
        return self.get_view(self.domain)

    def get_view(self, curr_dir):
        for next_dir in self.graph[curr_dir]:
            if '.html' in next_dir:
                yield '\t' + next_dir + '\n'
        for next_dir in sorted(self.graph[curr_dir]):
            if '.html' not in next_dir:
                yield self.get_view(next_dir)

    def print_graph_view(self):
        for line in self.get_graph_view():
            print(line)


graphDrawer = GraphDrawer()
graphDrawer.print_graph_view()