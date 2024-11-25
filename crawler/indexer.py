import logging
import asyncio
from urllib.parse import urlparse, urlunparse
from venv import logger

class Indexer:
    '''TODO ... 
    1. Stop words removal in text indexer
    2. Limitization / Standarisation of words in text index
    3. Correctly Formating urls in url index
    '''
    def __init__(self):
        self.url_index = {} # Key: source URL, Value: Set of destination URLs
        self.text_index = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Indexer")

    # def index(self, url, text, links):
    #     try:
    #         self.logger.info(f"Indexing URL: {url}")
    #         normalized_url = url.rstrip("/")

    #         # Index URLs (store the relationships)
    #         self.url_index[normalized_url] = links

    #         # Index text
    #         for word in text.split():
    #             self.text_index.setdefault(word, set()).add(url.rstrip("/"))
    #         # self.logger.info(self.text_index)
    #     except Exception as e:
    #         self.logger.error(f"Error indexing {url}: {str(e)}", exc_info=True)

    def normalize_url(self, url):
        parsed_url = urlparse(url)
        # Implement your URL normalization logic here
        # For example, you can remove query parameters, fragments, etc.
        normalized_url = urlunparse(parsed_url._replace(query=None, fragment=None))
        return normalized_url

    def index(self, url, text, links):
        try:
            normalized_url = self.normalize_url(url)
            self.logger.info(f"Indexing URL: {normalized_url}")

            # Index URLs (store the relationships)
            self.url_index[normalized_url] = links

            # Index text
            for word in text.split():
                self.text_index.setdefault(word, set()).add(normalized_url)

        except Exception as e:
            self.logger.error(f"Error indexing {url}: {str(e)}", exc_info=True)

        