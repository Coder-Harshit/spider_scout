import time
import asyncio
import concurrent.futures
import threading
from queue import Queue
from modules.robots_txt_handler import RobotsTxtHandler

class Scheduler:
    def __init__(self, url_frontier, downloaders, parsers, indexer, user_agent):
        self.url_frontier = url_frontier
        self.downloaders = downloaders
        self.parsers = parsers
        self.indexer = indexer
        self.robots_handler = RobotsTxtHandler(user_agent)
        self.current_depth = 0
        self.max_depth = 1
        self.downloader_queue = Queue()
        self.parsers_queue = Queue()

        # Inject scheduler reference into downloaders & parsers
        for downloader in self.downloaders:
            downloader.scheduler = self
        for parser in self.parsers:
            parser.scheduler = self
            parser.indexer = self.indexer


    def crawl(self, seed_url, depth=1):
        # self.max_depth = depth
        self.robots_handler.fetch_robots_txt(seed_url)
        start_time = time.time()
        self.url_frontier.add_url(seed_url)
        # self.url_frontier.add_url(seed_url, depth=0)
        
        # Start downloader and parser threads
        for downloader in self.downloaders:
            downloader.start()
        for parser in self.parsers:
            parser.start()
        
        # Main crawling loop
        while True:
            if self.url_frontier.has_next():
                url = self.url_frontier.get_next_url()
                # url, url_depth = self.url_frontier.get_next_url()
                # if url_depth > self.max_depth:
                    # continue # Skip URLs beyond max depth
                if self.robots_handler.is_allowed(url):
                    self.assign_downloader_task(url)
            else:
                # Check if all downloaders and parsers are idle
                if all(d.state == 'idle' for d in self.downloaders) and \
                   all(p.state == 'idle' for p in self.parsers):
                    break  # Exit the loop if all are idle
                time.sleep(0.1)
            self.current_depth += 1
        
        # Wait for downloader threads to finish
        for downloader in self.downloaders:
            downloader.join()
        # Wait for parser threads to finish
        for parser in self.parsers:
            parser.join()

        end_time = time.time()
        duration = end_time - start_time
        print(f"Crawling completed in {duration:.2f} seconds for depth {depth}")

    def assign_downloader_task(self, url):
        downloader_assigned = False
        while not downloader_assigned:
            for downloader in self.downloaders:
                if downloader.state == 'idle':
                    downloader.add_task(url)
                    # downloader.add_task(url, depth)
                    downloader_assigned = True
                    break
            if not downloader_assigned:
                time.sleep(0.1)

    # def process_url(self, url):
    #     try:
    #         downloader = self.get_idle_downloader()
    #         print(downloader)
    #         if downloader:
    #             html_content = downloader.fetch(url)
    #             downloader.state = 'idle'
            
    #             if html_content:
    #                 parser = self.get_idle_parser()
                    
    #                 if parser:
    #                     text, links, metadata = parser.parse(html_content, url)
    #                     parser.state = 'idle'
                        
    #                     asyncio.run(self.indexer.index(url, text, links))

    #                     for link in links:
    #                         self.url_frontier.add_url(link)

    #     except Exception as e:
    #         print(f"Error processing {url}: {e}")

    # def get_idle_downloader(self):
    #     while True:
    #         for downloader in self.downloaders:
    #             if downloader.state == 'idle':
    #                 downloader.state = 'running'
    #                 return downloader
    #         time.sleep(0.1)

    # def get_idle_parser(self):
        while True:
            for parser in self.parsers:
                if parser.state == 'idle':
                    parser.state = 'running'
                    return parser
            time.sleep(0.1)