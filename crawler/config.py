# crawler/config.py

import os

class Config:
    """Crawler configuration settings."""

    # User-Agent for requests
    USER_AGENT = "spider_scout/1.0 (+mailto:your_email@example.com)"

    # Maximum retries for failed requests
    MAX_RETRIES = 3

    # Delay between retries in seconds (exponential backoff)
    RETRY_DELAY = 2

    # Maximum depth for crawling
    MAX_CRAWL_DEPTH = 3

    # Directory to save logs and crawled data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Allowed domains for crawling
    ALLOWED_DOMAINS = [
        "example.com",
        "testsite.com",
    ]

    # Seed URLs
    SEED_URLS = [
        "https://example.com",
        "https://testsite.com",
    ]

    # Database configuration
    DATABASE = {
        "name": "crawler.db",
        "path": os.path.join(BASE_DIR, "crawler.db"),
    }

    # Create necessary directories
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)
