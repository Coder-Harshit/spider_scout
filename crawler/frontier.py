import queue
import logging

class URLFrontier:
    def __init__(self):
        self.frontier = queue.PriorityQueue()
        self.visited = set()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized URLFrontier")

    def add_url(self, url, priority=0):
        if url not in self.visited:
            self.frontier.put((priority, url))
            self.visited.add(url)
            self.logger.info(f"Added URL to frontier: {url}")

    def has_next(self):
        return not self.frontier.empty()

    def get_next_url(self):
        return self.frontier.get()[1]
