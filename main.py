import sys
import json
from crawler.frontier import URLFrontier
from crawler.downloader import Downloader
from crawler.parser import Parser
from crawler.indexer import Indexer
from crawler.scheduler import Scheduler
from crawler.robots_txt_handler import RobotsTxtHandler
import crawler.logger_config

# Setup logger
logger = crawler.logger_config.setup_logger()

# Configuration
N = 5  # Number of downloader and parser threads
USER_AGENT = "spider_scout/1.0 (+mailto:your_email@example.com)"

# Initialize components
URL_FRONTIER = URLFrontier()
DOWNLOADER_POOL = [Downloader(USER_AGENT) for _ in range(N)]
PARSER_POOL = [Parser() for _ in range(N)]
INDEXER = Indexer()
ROBOTS_TXT_HANDLER = RobotsTxtHandler(USER_AGENT)

# Print progress callback
def print_progress(current, total):
    """Send crawling progress to frontend"""
    progress = min(100, int((current / max(1, total)) * 100))
    print(json.dumps({"type": "progress", "value": progress}), flush=True)

# Print crawled result callback
def print_result(url):
    """Send crawled URL result to frontend"""
    print(json.dumps({"type": "result", "url": url}), flush=True)

# Scheduler initialization
SCHEDULER = Scheduler(
    URL_FRONTIER,
    DOWNLOADER_POOL,
    PARSER_POOL,
    INDEXER,
    ROBOTS_TXT_HANDLER,
    progress_callback=print_progress,
    result_callback=print_result
)
# Set the scheduler attribute for each downloader and parser
for downloader in DOWNLOADER_POOL:
    downloader.scheduler = SCHEDULER

for parser in PARSER_POOL:
    parser.scheduler = SCHEDULER
    parser.indexer = INDEXER

# Main program entry point
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <url> <depth> <respect_robots_txt>")
        sys.exit(1)

    # Command line arguments
    seed_url = sys.argv[1]
    depth = int(sys.argv[2])
    respect_robots_txt = sys.argv[3] == '1'

    # Start crawling
    logger.info(f"Starting crawl for {seed_url} with depth {depth}, respect robots.txt: {respect_robots_txt}")
    SCHEDULER.crawl(seed_url, max_depth=depth, respect_robots_txt=respect_robots_txt)
