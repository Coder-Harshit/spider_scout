import logging
import asyncio

class Indexer:
    '''TODO ... 
    1. Stop words removal in text indexer
    2. Limitization / Standarisation of words in text index
    3. Correctly Formating urls in url index
    '''
    def __init__(self):
        self.url_index = {}
        self.text_index = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Indexer")

    def index(self, url, text, links):
        try:
            self.logger.info(f"Indexing URL: {url}")
            # Index URLs
            for link in links:
                self.url_index.setdefault(link, set()).add(url.rstrip("/"))

            # Index text
            for word in text.split():
                self.text_index.setdefault(word, set()).add(url.rstrip("/"))
        except Exception as e:
            self.logger.error(f"Error indexing {url}: {str(e)}", exc_info=True)