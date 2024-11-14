import time
import asyncio
import concurrent.futures

class Scheduler:
    def __init__(self, url_frontier, downloaders, parsers, indexer):
        self.url_frontier = url_frontier
        self.downloaders = downloaders
        self.parsers = parsers
        self.indexer = indexer

    def crawl(self, seed_url, depth=1):
        start_time = time.time()
        
        count = 0
        self.url_frontier.add_url(seed_url)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            while self.url_frontier.has_next() and count < depth:
                url = self.url_frontier.get_next_url().rstrip("/")
                futures.append(executor.submit(self.process_url, url))
                
                count+=1

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing URL: {e}")

        end_time = time.time()
        duration = end_time - start_time
        print(f"Crawling completed in {duration:.2f} seconds for depth {depth}")


    def process_url(self, url):
        try:
            downloader = self.get_idle_downloader()
            if downloader:
                html_content = downloader.fetch(url)
                downloader.state = 'idle'
            
                if html_content:
                    parser = self.get_idle_parser()
                    
                    if parser:
                        text, links, metadata = parser.parse(html_content, url)
                        parser.state = 'idle'
                        
                        asyncio.run(self.indexer.index(url, text, links))

                        for link in links:
                            self.url_frontier.add_url(link)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    def get_idle_downloader(self):
        while True:
            for downloader in self.downloaders:
                if downloader.state == 'idle':
                    downloader.state = 'running'
                    return downloader
            time.sleep(0.1)

    def get_idle_parser(self):
        while True:
            for parser in self.parsers:
                if parser.state == 'idle':
                    parser.state = 'running'
                    return parser
            time.sleep(0.1)