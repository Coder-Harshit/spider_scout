import requests

class Downloader:
    def fetch(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        
        except requests.exceptions.RequestException as err:
            print(f"Error Fetching {url}: {err}")
            return None