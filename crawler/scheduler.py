# import time
# from queue import Queue

# class Scheduler:
#     def __init__(self, url_frontier, downloaders, parsers, indexer):
#         self.url_frontier = url_frontier
#         self.downloaders = downloaders
#         self.parsers = parsers
#         self.indexer = indexer
#         self.downloader_queue = Queue()
#         self.parsers_queue = Queue()

#         for downloader in self.downloaders:
#             downloader.scheduler = self
#         for parser in self.parsers:
#             parser.scheduler = self
#             parser.indexer = self.indexer

#     def crawl(self, seed_url, depth=1):
#         self.url_frontier.add_url(seed_url)
#         for downloader in self.downloaders:
#             downloader.start()
#         for parser in self.parsers:
#             parser.start()

#         while self.url_frontier.has_next():
#             url = self.url_frontier.get_next_url()
#             self.downloader_queue.put(url)
#             time.sleep(0.1)

#         for downloader in self.downloaders:
#             downloader.join()
#         for parser in self.parsers:
#             parser.join()
