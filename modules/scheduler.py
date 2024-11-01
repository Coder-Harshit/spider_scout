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

            try:
                html_content = self.downloader.fetch(url)
                if html_content:
                    text, links, metadata = self.parser.parse(html_content)

                    self.indexer.index(url, text, links)

                    #for debugging stoping here (unless depth limit has been implemented)
                    break

                    for link in links:
                        self.url_frontier.add_url(link)
            
            except Exception as e:
                print(f"Error processing {url}: {e}")