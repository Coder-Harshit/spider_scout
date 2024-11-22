import logging
import asyncio

class Indexer:
    def __init__(self):
        self.url_index = {}
        self.text_index = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Indexer")

    async def index(self, url, text, links):
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
