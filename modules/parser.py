import asyncio
import queue
from bs4 import BeautifulSoup
import re
import logging
import threading
import time

class Parser(threading.Thread):
    def __init__(self):
        super().__init__()
        self.state = 'idle'
        self.logger = logging.getLogger(__name__)
        self.indexer = None
        self.task_queue = []
        self.lock = threading.Lock()
        self.logger.debug("Initialized Parser")

    def run(self):
        while True:
            try:
                task = self.scheduler.parsers_queue.get(timeout=1)
                if task:
                    self.state = 'running'
                    html_content, root_url = task
                    # html_content, root_url, depth = task
                    text, links, metadata = self.parse(html_content, root_url)
                    self.state = 'idle'
                    # Asynchronously index the parsed data
                    # asyncio.run(self.indexer.index(root_url, text, links, metadata))
                    asyncio.run(self.indexer.index(root_url, text, links))
                    # Add new links to the frontier
                    for link in links:
                        self.scheduler.url_frontier.add_url(link)
                        # self.scheduler.url_frontier.add_url(link, depth=depth+1)
                else:
                    time.sleep(0.1)
            except queue.Empty:
                time.sleep(0.1)


    def parse(self, html_content, root_url):
        try:
            self.logger.info(f"Parsing HTML content")
            soup = BeautifulSoup(html_content, 'html.parser')
            textual_content = soup.get_text()
            links = set()

            for link in soup.find_all('a'):
                # in all anchor tags
                href = link.get('href')
                if href:
                    if re.search("^http",href):
                        links.add(href.rstrip("/"))
                    else:
                        links.add((root_url+href).rstrip("/"))
            
            # metadata
            title = soup.title.text if soup.title else None
            
            desc_tag = soup.find('meta', attrs={'name':'description'})
            desc = desc_tag['content'] if desc_tag else None
            
            metadata = {
                'title':title,
                'description':desc
            }

            # #####
            # print(f"Extracted text: {textual_content}", file=open('spiderscout.log', 'a'))
            # print(f"Extracted links: {links}", file=open('spiderscout.log', 'a'))
            # print(f"Extracted metadata: {metadata}", file=open('spiderscout.log', 'a'))
            # #######################################

            return textual_content, links, metadata

        except Exception as e:
            self.logger.error(f"Error parsing HTML content: {str(e)}", exc_info=True)

    def add_task(self, html_content, root_url):
        with self.lock:
            self.task_queue.append((html_content, root_url))