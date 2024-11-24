import threading
import time
import logging
from queue import Queue, Empty
from crawler import downloader

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

    # def crawl(self, seed_url, max_depth, respect_robots_txt=True):
    #     try:
    #         # Initialize crawling
    #         self.logger.info("Starting crawl...")
    #         self.url_frontier.add_url(seed_url)
    #         if respect_robots_txt:
    #             self.robots_txt_handler.fetch_robots_txt(seed_url)

    #         # Start worker threads
    #         for worker in self.downloaders + self.parsers:
    #             worker.start()

    #         processed_urls = 0
    #         total_urls = max_depth
    #         print(max_depth)
    #         while processed_urls < total_urls:
    #             print(processed_urls)
    #             self.url_frontier.display()
    #             try:
    #                 url = self.url_frontier.get_next_url()
    #                 print(url)
    #                 if url is None:
    #                     break

    #                 if (not respect_robots_txt) or (self.robots_txt_handler.is_allowed(url)):
    #                     status = self.downloader_assignment(url)
    #                     while not status:
    #                         # Find an available downloader
    #                         time.sleep(1)
    #                         status = self.downloader_assignment(url)
    #                     processed_urls += 1

    #                     if self.progress_callback:
    #                         self.progress_callback(processed_urls, total_urls)

    #             except Exception as e:
    #                 self.logger.error(f"Error during scheduling: {e}")

    #         # Wait for queues and signal termination
    #         self.stop_event.set()
    #         self.downloader_queue.join()
    #         self.parsers_queue.join()

    #         for _ in self.downloaders + self.parsers:
    #             self.downloader_queue.put(None)
    #             self.parsers_queue.put(None)

    #         for worker in self.downloaders + self.parsers:
    #             worker.join()

    #         if self.progress_callback:
    #             self.progress_callback(total_urls, total_urls)

    #     except Exception as e:
    #         self.logger.error(f"Crawl failed: {e}", exc_info=True)
    #     finally:
    #         self.logger.info("Crawl completed.")

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

            # total_urls = 1  # Start with the seed URL
            # processed_urls = 0

            while True:
                # # Check if max depth reached
                # if processed_urls >= max_depth:
                #     break

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