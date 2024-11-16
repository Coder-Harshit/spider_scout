import logging
import requests
import time

class Downloader:
    def __init__(self, user_agent, delay=1):
        self.logger = logging.getLogger(__name__)
        self.user_agent = user_agent
        self.delay = delay
        self.state = 'idle'
        self.logger.debug(f"Initalized Downloader with user_agent: {user_agent}")

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
                    # print(f"Error Fetching {url}: {err}")
                    time.sleep(self.delay * (2**attempt))
            return None
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}",exc_info=True)