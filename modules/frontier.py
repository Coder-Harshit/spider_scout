from queue import PriorityQueue


class URLFrontier:
    def __init__(self):
        self.frontier = PriorityQueue()
        self.visited = set()

    def add_url(self, url, priority=0):
        #######################################
        # logging
        print(f"Adding URL to frontier: {url}", file=open('spiderscout.log', 'a'))
        #######################################
        self.frontier.put(url)
        if url not in self.visited:
            self.frontier.put((priority,url))
            self.visited.add(url)
    
    def has_next(self):
        return not self.frontier.empty()
    
    def get_next_url(self):
        fetched_priority, fetched_url = self.frontier.get()
        return fetched_url