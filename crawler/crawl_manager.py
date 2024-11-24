import logging
import threading
from time import sleep
from downloader import Downloader
from parser import Parser
from scheduler import Scheduler

class CrawlManager:
    def __init__(self, scheduler, downloader, parser, max_threads=5, crawl_delay=1):
        """
        Initializes the CrawlManager with the scheduler, downloader, parser, and thread configuration.
        
        Args:
            scheduler (Scheduler): The scheduler instance managing the URL queue.
            downloader (Downloader): The downloader instance to fetch web pages.
            parser (Parser): The parser instance to extract data from web pages.
            max_threads (int): Maximum number of threads for crawling concurrently.
            crawl_delay (int): Delay between each crawl in seconds to control crawl rate.
        """
        self.scheduler = scheduler
        self.downloader = downloader
        self.parser = parser
        self.max_threads = max_threads
        self.crawl_delay = crawl_delay
        self.logger = logging.getLogger(__name__)
        self.logger.debug("CrawlManager initialized")

    def crawl(self):
        """
        Starts the crawling process, creating multiple threads to download and parse URLs concurrently.
        """
        self.logger.info("Crawl process started")

        threads = []
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self._crawl_worker)
            thread.daemon = True  # Ensures threads exit when the program ends
            thread.start()
            threads.append(thread)

        # Wait for threads to complete (this can be adjusted based on the desired behavior)
        for thread in threads:
            thread.join()

    def _crawl_worker(self):
        """
        Worker method for each crawling thread. It continuously fetches URLs from the queue and processes them.
        """
        while not self.scheduler.is_queue_empty():
            url = self.scheduler.get_next_url()
            if url:
                self.logger.info(f"Processing URL: {url}")
                page_content = self.downloader.download(url)
                if page_content:
                    self.logger.debug(f"Page content for {url} downloaded successfully")
                    parsed_data = self.parser.parse(page_content, url)
                    self._handle_parsed_data(parsed_data)
                sleep(self.crawl_delay)  # Respect the crawl delay between requests

    def _handle_parsed_data(self, parsed_data):
        """
        Handles the parsed data after extracting it from a web page. This can include saving data, 
        processing further links, or logging errors if parsing fails.
        
        Args:
            parsed_data (dict): The parsed data returned by the parser.
        """
        if parsed_data:
            self.logger.info(f"Data extracted: {parsed_data}")
            # Further actions on the parsed data can go here, like saving to a database
        else:
            self.logger.warning("No data parsed from the page")

    def stop(self):
        """
        Stops the crawling process and joins all threads.
        """
        self.logger.info("Crawl process stopped")
        # Additional cleanup can be done here if needed
