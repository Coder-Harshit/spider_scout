from queue import PriorityQueue
import logging

class URLFrontier:
    def __init__(self):
        self.frontier = PriorityQueue()
        self.visited = set()
        # self.visited = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized URLFrontier")

    def add_url(self, url, priority=0):
        if url not in self.visited:
        # if url not in self.visited or self.visited[url] < depth:
            try:
                self.logger.info(f"Adding URL to frontier: {url}")
                self.frontier.put((priority,url))
                self.visited.add(url)
                # self.visited[url] = depth
            except Exception as e:
                self.logger.error(f"Error adding URL to frontier: {str(e)}", exc_info=True)
                
    def has_next(self):
        return not self.frontier.empty()
    
    def get_next_url(self):
        fetched_priority, fetched_url = self.frontier.get()
        return fetched_url