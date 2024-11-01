import requests
import time

class Downloader:
    def __init__(self, user_agent, delay=1):
        self.user_agent = user_agent
        self.delay = delay

    def fetch(self, url, max_attempts=3):
        #######################################
        # logging
        print(f"Fetching URL: {url}", file=open('spiderscout.log', 'a'))        #######################################

        headers = {'User-Agent':self.user_agent}
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                return response.text
            
            except requests.exceptions.RequestException as err:
                print(f"Error Fetching {url}: {err}")
                time.sleep(self.delay * (2**attempt))
            return None