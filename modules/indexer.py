import asyncio
import logging

class Indexer:
    def __init__(self):
        # dict for inverted index
        self.url_index = {}
        self.text_index = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Indexer")

    async def index(self, url, text, links):
        try:
            self.logger.info(f"Indexing URL: {url}")
            # Index URLs
            for link in links:
                if link not in self.url_index:
                    self.url_index[link] = set()
                self.url_index[link].add(url.rstrip("/"))

            # Index text
            for word in text.split():
                if word not in self.text_index:
                    self.text_index[word] = set()
                self.text_index[word].add(url.rstrip("/"))
        except Exception as e:
            self.logger.error(f"Error indexing {url}: {str(e)}", exc_info=True)
        