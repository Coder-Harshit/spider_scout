class Scheduler:
    def __init__(self, url_frontier, downloader, parser, indexer):
        self.url_frontier = url_frontier
        self.downloader = downloader
        self.parser = parser
        self.indexer = indexer

    def crawl(self, seed_url):
        self.url_frontier.add_url(seed_url)
        while self.url_frontier.has_next():
            url = self.url_frontier.get_next_url()
            html_content = self.downloader.fetch(url)
            extracted_data = self.parser.parse(html_content)
            self.indexer.index(url, extracted_data)