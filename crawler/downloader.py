import logging
import queue
import time
import requests
import threading
from queue import Queue
from urllib.parse import urlparse


class Downloader(threading.Thread):
    def __init__(self, user_agent, scheduler=None, delay=1):
        super().__init__()
        self.user_agent = user_agent
        self.scheduler = scheduler
        self.delay = delay
        self.state = 'idle'
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initialized Downloader with user_agent: {user_agent}")
        
    def run(self):
        while True:
            try:
                task = self.scheduler.downloader_queue.get(timeout=1)  # Waiting for a task from the queue
                if task is None:
                    # 
                    self.scheduler.downloader_queue.task_done()
                    # 
                    break

                self.state = 'running'
                url, depth = task
                html_content = self.fetch(url)
                if html_content:
                    self.scheduler.parsers_queue.put((html_content, url, depth))  # Forwarding the html content to the parser queue
                self.state = 'idle'
                
                self.scheduler.downloader_queue.task_done()  # Mark the task as done
            except queue.Empty:
                continue 
            except Exception as e:
                self.logger.error(f"Error in downloader run loop: {str(e)}")

    def fetch(self, url, max_attempts=3):
        """
        Fetches the URL and returns the HTML content if successful.
        Retries up to `max_attempts` in case of failure.
        """
        headers = {'User-Agent': self.user_agent}
        for attempt in range(max_attempts):
            try:
                self.logger.info(f"Attempt {attempt + 1} Fetching: {url}")
                response = requests.get(url, headers=headers, timeout=10)  # Using a 10 second timeout for requests
                response.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)
                
                self.logger.info(f"Successfully fetched: {url}")
                return response.text  # Return the HTML content of the page

            except requests.RequestException as err:
                self.logger.error(f"Error fetching {url}: {str(err)}")
                if attempt < max_attempts - 1:
                    # Implementing exponential backoff on retries
                    time.sleep(self.delay * (2 ** attempt))
                else:
                    self.logger.error(f"Failed to fetch {url} after {max_attempts} attempts")
                    return None  # Return None if it fails after all attempts

