import threading
import time
import logging
from queue import Queue

class Scheduler:
    def __init__(self, url_frontier, downloaders, parsers, indexer, robots_txt_handler=None, progress_callback=None, result_callback=None):
        self.url_frontier = url_frontier
        self.downloaders = downloaders
        self.parsers = parsers
        self.indexer = indexer
        self.robots_txt_handler = robots_txt_handler
        self.downloader_queue = Queue()
        self.parsers_queue = Queue()
        self.stop_event = threading.Event()
        self.progress_callback = progress_callback
        self.result_callback = result_callback
        self.logger = logging.getLogger(__name__)

    def downloader_assignment(self, url):
        downloader_assigned = False
        for _ in range(len(self.downloaders)):
            downloader = next(
                (d for d in self.downloaders if d.state == 'idle'),
                None
            )
            if downloader:
                self.downloader_queue.put(url)
                downloader_assigned = True
                break
        return downloader_assigned

    def crawl(self, seed_url, max_depth, respect_robots_txt=True):
        try:
            # Initialize crawling
            self.logger.info("Starting crawl...")
            self.url_frontier.add_url(seed_url, depth=0)
            if respect_robots_txt:
                self.robots_txt_handler.fetch_robots_txt(seed_url)

            # Start worker threads
            for worker in self.downloaders + self.parsers:
                worker.start()

            while True:
                # Try to get next URL from frontier
                url, depth = self.url_frontier.get_next_url()
                if url is not None and depth is not None:
                    if depth > max_depth:
                        continue  # Skip URLs beyond max depth
                    if (not respect_robots_txt) or (self.robots_txt_handler.is_allowed(url)):
                        self.downloader_queue.put((url, depth))  # Pass depth to downloader
                    if self.progress_callback:
                        self.progress_callback(depth, max_depth)
                else:
                    # No URLs left to process
                    if self.downloader_queue.empty() and self.parsers_queue.empty():
                        all_idle = all(downloader.state == 'idle' for downloader in self.downloaders) and \
                                   all(parser.state == 'idle' for parser in self.parsers)
                        if all_idle:
                            break
                    else:
                        time.sleep(1)

            # Signal termination
            for _ in self.downloaders:
                self.downloader_queue.put(None)
            for _ in self.parsers:
                self.parsers_queue.put(None)

            for worker in self.downloaders + self.parsers:
                worker.join()

            self.logger.info("Crawl completed.")

        except Exception as e:
            self.logger.error(f"Crawl failed: {e}", exc_info=True)