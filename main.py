import sys
import json
from crawler.downloader import Downloader
from crawler.parser import Parser
from crawler.indexer import Indexer
from crawler.scheduler import Scheduler
from crawler.frontier import URLFrontier

USER_AGENT = "spider_scout/1.0 (+mailto:your_email@example.com)"
DOWNLOADER_POOL = [Downloader(USER_AGENT) for _ in range(5)]
PARSER_POOL = [Parser() for _ in range(5)]
URL_FRONTIER = URLFrontier()
INDEXER = Indexer()
SCHEDULER = Scheduler(URL_FRONTIER, DOWNLOADER_POOL, PARSER_POOL, INDEXER, USER_AGENT)

def print_progress(progress):
    print(json.dumps({"type": "progress", "value": progress}), flush=True)

def print_result(url):
    print(json.dumps({"type": "result", "url": url}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <url> <depth> <respect_robots_txt>")
        sys.exit(1)

    seed_url = sys.argv[1]
    depth = int(sys.argv[2])
    # respect_robots_txt = sys.argv[3] == '1'
    SCHEDULER.crawl(seed_url, depth=depth)
    # scheduler.crawl(url, depth=depth, respect_robots_txt=respect_robots_txt, progress_callback=print_progress, result_callback=print_result)