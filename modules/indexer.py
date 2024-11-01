class Indexer:
    def __init__(self):
        # dict for inverted index
        self.url_index = {}
        self.text_index = {}

    def index(self, url, text, links):
        # Index URLs
        for link in links:
            if link not in self.url_index:
                self.url_index[link] = set()
            self.url_index[link].add(url)

        # Index text
        for word in text.split():
            if word not in self.text_index:
                self.text_index[word] = set()
            self.text_index[word].add(url)