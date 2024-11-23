import time
from queue import Queue

class Scheduler:
    def __init__(self, url_frontier, downloaders, parsers, indexer, robots_txt_handler):
        self.url_frontier = url_frontier
        self.downloaders = downloaders
        self.parsers = parsers
        self.indexer = indexer
        self.robots_txt_handler = robots_txt_handler
        self.downloader_queue = Queue()
        self.parsers_queue = Queue()

        for downloader in self.downloaders:
            downloader.scheduler = self
        for parser in self.parsers:
            parser.scheduler = self
            parser.indexer = self.indexer

    def crawl(self, seed_url, depth=1):
        try:
            self.url_frontier.add_url(seed_url)
            self.robots_txt_handler.fetch_robots_txt(seed_url)
            
            # Start worker threads
            for downloader in self.downloaders:
                downloader.start()
            for parser in self.parsers:
                parser.start()

            processed_urls = 0
            while processed_urls < depth and self.url_frontier.has_next():
                url = self.url_frontier.get_next_url()
                if self.robots_txt_handler.is_allowed(url):
                    self.downloader_queue.put(url)
                    processed_urls += 1

            # Wait for queues to be processed
            self.downloader_queue.join()
            self.parsers_queue.join()

            # Signal threads to terminate
            for _ in self.downloaders:
                self.downloader_queue.put(None)
            for _ in self.parsers:
                self.parsers_queue.put(None)

            # Wait for threads to finish
            for downloader in self.downloaders:
                downloader.join()
            for parser in self.parsers:
                parser.join()

        except Exception as e:
            self.logger.error(f"Error in crawler: {str(e)}", exc_info=True)