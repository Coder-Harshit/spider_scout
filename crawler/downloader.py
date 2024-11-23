import queue
import threading
import time
import logging
import requests

class Downloader(threading.Thread):
    def __init__(self, user_agent, delay=1):
        super().__init__()
        self.user_agent = user_agent
        self.delay = delay
        self.state = 'idle'
        self.scheduler = None
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initialized Downloader with user_agent: {user_agent}")

    def run(self):
        while True:
            try:
                task = self.scheduler.downloader_queue.get(timeout=1)
                if task is None:
                    break
                self.state = 'running'
                html_content = self.fetch(task)
                if html_content:
                    self.scheduler.parsers_queue.put((html_content, task))
                self.state = 'idle'
                
                # Mark task as done
                self.scheduler.downloader_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in downloader run loop: {str(e)}")
            # finally:
            #     self.scheduler.downloader_queue.task_done()
            #     # time.sleep(0.1)
            # Don't mark as done if we didn't get a task

    def fetch(self, url, max_attempts=3):
        headers = {'User-Agent': self.user_agent}
        for attempt in range(max_attempts):
            try:
                self.logger.info(f"Attempt {attempt + 1} Fetching: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                self.scheduler.parsers_queue.put((response.text, url))
                
                # RESPONSE.TEXT => full html file code
                return response.text
            
            except requests.RequestException as err:
                self.logger.error(f"Error fetching {url}: {str(err)}")
                if attempt < max_attempts - 1:
                    time.sleep(self.delay * (2 ** attempt))
                else:
                    self.logger.error(f"Failed to fetch {url} after {max_attempts} attempts")