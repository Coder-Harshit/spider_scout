import queue
import logging
import threading
from urllib.parse import urlparse

class URLFrontier:
    def __init__(self):
        self.frontier = queue.PriorityQueue()
        self.visited = set()
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized URLFrontier")

    def display(self):
        print("VISITED:\n", self.visited)
        print("FRONTIER:")
        with self.lock:
            frontier_list = list(self.frontier.queue)
            for item in frontier_list:
                print(item)
    # def add_url(self, url, priority=0):
    #     if url not in self.visited:
    #         self.frontier.put((priority, url))
    #         self.visited.add(url)
    #         self.logger.info(f"Added URL to frontier: {url}")

    def add_url(self, url, depth, priority=0):
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                normalized_url = url.rstrip('/')
                with self.lock:
                    if normalized_url not in self.visited:
                        
                        # FOR BFS TRAVERSAL
                        ## When adding URLs to the frontier
                        # priority = depth  # Lower depth gets higher priority (processed earlier)
                        # self.frontier.put((priority, depth, url))
                        
                        self.frontier.put((priority, depth, normalized_url))
                        self.visited.add(normalized_url)
                        # self.logger.info(f"Added URL: {normalized_url}")
        except Exception as e:
            self.logger.error(f"Error adding URL to frontier: {str(e)}")
    
    def is_empty(self):
        with self.lock:
            return self.frontier.empty()

    def has_next(self):
        with self.lock:
            return not self.frontier.empty()

    def get_next_url(self):
        with self.lock:
            if not self.frontier.empty():
                _,depth, url = self.frontier.get()
                # self.visited.add(url)
                return url, depth
            else:
                return None, None
