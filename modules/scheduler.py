class Scheduler:
    def __init__(self, url_frontier, downloader, parser, indexer):
        self.url_frontier = url_frontier
        self.downloader = downloader
        self.parser = parser
        self.indexer = indexer

    def crawl(self, seed_url):
        self.url_frontier.add_url(seed_url)

        while not self.url_frontier.is_empty():
            url = self.url_frontier.get_next_url()

            try:
                html_content = self.downloader.fetch(url)
                if html_content:
                    text, links, metadata = self.parser.parse(html_content)

                    self.indexer.index(url, text, links, metadata)
                    
                    for link in links:
                        self.url_frontier.add_url(link)
            
            except Exception as e:
                print(f"Error processing {url}: {e}")