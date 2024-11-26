import queue
import threading
import logging
from bs4 import BeautifulSoup
from crawler.util import normalize_url

class Parser(threading.Thread):
    def __init__(self, scheduler=None, indexer=None):
        super().__init__()
        self.state = 'idle'
        self.logger = logging.getLogger(__name__)
        self.indexer = indexer
        self.scheduler = scheduler
        self.logger.debug("Initialized Parser")

    def run(self):
        while True:
            try:
                task = self.scheduler.parsers_queue.get(timeout=1)
                if task is None:
                    # 
                    self.scheduler.parsers_queue.task_done()
                    # 
                    break
                self.state = 'running'
                html_content, root_url, current_depth = task
                text, links, metadata = self.parse(html_content, root_url)

                # adding it to frontier:
                for link in links:
                    self.scheduler.url_frontier.add_url(link, current_depth+1)
                    
                self.scheduler.url_frontier.display()

                # Synchronous indexing instead of async
                self.indexer.index(root_url, text, links)
                self.state = 'idle'

                # Mark task as done
                self.scheduler.parsers_queue.task_done()
                
            except queue.Empty:
                continue # Don't break, keep waiting for tasks
            except Exception as e:
                self.logger.error(f"Error in parser run loop: {str(e)}")

    def parse(self, html_content, root_url):
        try:
            self.logger.info(f"Parsing HTML content from {root_url}")
            soup = BeautifulSoup(html_content, 'html.parser')

            textual_content = soup.get_text()

            links = set()
            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                # Normalize the URL
                normalized_url = normalize_url(root_url, href)
                links.add(normalized_url)
            
            metadata = {
                "title": soup.title.text if soup.title else None,
                "description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content"),
            }

            return textual_content, links, metadata
        
        except Exception as e:
            self.logger.error(f"Error parsing HTML content: {str(e)}", exc_info=True)
            return "", set(), {}

    def add_task(self, html_content, root_url):
        self.scheduler.parsers_queue.put((html_content, root_url))
