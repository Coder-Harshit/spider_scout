import queue
import logging
from urllib.parse import urlparse

class URLFrontier:
    def __init__(self):
        self.frontier = queue.PriorityQueue()
        self.visited = set()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized URLFrontier")

    # def add_url(self, url, priority=0):
    #     if url not in self.visited:
    #         self.frontier.put((priority, url))
    #         self.visited.add(url)
    #         self.logger.info(f"Added URL to frontier: {url}")

    def add_url(self, url, priority=0):
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                normalized_url = url.rstrip('/')
                if normalized_url not in self.visited:
                    self.frontier.put((priority, normalized_url))
                    self.visited.add(normalized_url)
                    self.logger.info(f"Added URL to frontier: {normalized_url}")
        except Exception as e:
            self.logger.error(f"Error adding URL to frontier: {str(e)}")

    def has_next(self):
        return not self.frontier.empty()

    def get_next_url(self):
        return self.frontier.get()[1]
