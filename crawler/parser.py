import threading
import logging
import time
from bs4 import BeautifulSoup
import re
import asyncio

class Parser(threading.Thread):
    def __init__(self):
        super().__init__()
        self.state = 'idle'
        self.logger = logging.getLogger(__name__)
        self.indexer = None
        self.scheduler = None
        self.logger.debug("Initialized Parser")

    def run(self):
        while True:
            try:
                task = self.scheduler.parsers_queue.get(timeout=1)
                if task:
                    self.state = 'running'
                    html_content, root_url = task
                    text, links, metadata = self.parse(html_content, root_url)
                    asyncio.run(self.indexer.index(root_url, text, links))
                    for link in links:
                        self.scheduler.url_frontier.add_url(link)
                    self.state = 'idle'
            except Exception as e:
                self.logger.error(f"Error in parser run loop: {str(e)}")
            finally:
                time.sleep(0.1)

    def parse(self, html_content, root_url):
        try:
            self.logger.info(f"Parsing HTML content from {root_url}")
            soup = BeautifulSoup(html_content, 'html.parser')
            textual_content = soup.get_text()
            links = {
                (root_url + href).rstrip("/")
                if not href.startswith("http") else href.rstrip("/")
                for href in (link.get("href") for link in soup.find_all("a")) if href
            }

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
