import logging
import requests
import time
import threading

class Downloader(threading.Thread):
    def __init__(self, user_agent, delay=1):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.user_agent = user_agent
        self.delay = delay
        self.state = 'idle'
        self.task_queue = []
        self.lock = threading.Lock()
        self.logger.debug(f"Initalized Downloader with user_agent: {user_agent}")

    def run(self):
        while True:
            url = None
            # url,depth = None, None
            with self.lock:
                if self.task_queue:
                    # url, depth = self.task_queue.pop(0)
                    url = self.task_queue.pop(0)
            
            if url:
                self.state = 'running'
                html_content = self.fetch(url)
                self.state = 'idle'
                if html_content:
                    self.scheduler.parsers_queue.put((html_content, url))
            else:
                time.sleep(0.1)

    def fetch(self, url, max_attempts=3):
        try:
            self.logger.info(f"Fetching URL: {url}")
            headers = {'User-Agent':self.user_agent}
            for attempt in range(max_attempts):
                try:
                    self.logger.info(f"Attempt {attempt+1} Downloading: {url}")
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    return response.text
                
                except requests.exceptions.RequestException as err:
                    self.logger.error(f"Error Fetching {url}: {str(err)}",exc_info=True)
                    time.sleep(self.delay * (2**attempt))
            return None
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}",exc_info=True)
    
    def add_task(self, url):
        with self.lock:
            self.task_queue.append(url)
            # self.task_queue.append(url, depth)