import logging
from urllib.parse import urlparse, urlunparse
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import nltk

# Downloading necessary NLTK data files
nltk.download('stopwords')
nltk.download('wordnet')

class Indexer:
    def __init__(self, use_lemmatizer=False):
        self.url_index = {}  # Key: source URL, Value: Set of destination URLs
        self.text_index = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Indexer")
        self.stop_words = set(stopwords.words('english'))
        self.use_lemmatizer = use_lemmatizer
        if use_lemmatizer:
            self.processor = WordNetLemmatizer()
        else:
            self.processor = PorterStemmer()

    def normalize_url(self, url):
        '''
        Normalizes the URL by removing the query parameters and fragments.        
        '''
        parsed_url = urlparse(url)
        normalized_url = urlunparse(parsed_url._replace(query=None, fragment=None))
        return normalized_url

    def process_text(self, text):
        '''
        => Lemmatizer:
            Purpose: Reduces words to their base or root form, known as the lemma.
            Example: "running" → "run", "better" → "good".
            Accuracy: More accurate because it considers the context and the part of speech of the word.
            Use Case: Suitable for applications where the meaning of the word is important, such as natural language processing tasks, information retrieval, and text analysis.

        => Stemmer:
            Purpose: Reduces words to their root form by chopping off the ends.
            Example: "running" → "run", "better" → "better".
            Accuracy: Less accurate because it doesn't consider the context or part of speech.
            Use Case: Suitable for applications where speed is more important than accuracy, such as simple search engines or indexing large volumes of text.

        => Why Stemmer given priority over Lemmatizer ? 
            In our case stemming is given priority over lemmatizing due to the speed of operation of stemming over lemmitizing, and since our crawller is more focused on indexing and searching the web pages, the speed of operation is more important than the accuracy of the words.

        '''
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        if self.use_lemmatizer:
            processed_words = [self.processor.lemmatize(word.lower()) for word in filtered_words]
        else:
            processed_words = [self.processor.stem(word.lower()) for word in filtered_words]
        return processed_words

    def index(self, url, text, links):
        try:
            normalized_url = self.normalize_url(url)
            self.logger.info(f"Indexing URL: {normalized_url}")

            # Index URLs (store the relationships)
            self.url_index[normalized_url] = links

            # Index text
            processed_words = self.process_text(text)
            for word in processed_words:
                self.text_index.setdefault(word, set()).add(normalized_url)

        except Exception as e:
            self.logger.error(f"Error indexing {url}: {str(e)}", exc_info=True)
