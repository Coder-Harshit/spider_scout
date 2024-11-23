import sys
import json
from crawler.frontier import URLFrontier
from crawler.downloader import Downloader
from crawler.parser import Parser
from crawler.indexer import Indexer
from crawler.scheduler import Scheduler
from crawler.robots_txt_handler import RobotsTxtHandler

USER_AGENT = "spider_scout/1.0 (+mailto:your_email@example.com)"
DOWNLOADER_POOL = [Downloader(USER_AGENT) for _ in range(5)]
PARSER_POOL = [Parser() for _ in range(5)]
URL_FRONTIER = URLFrontier()
INDEXER = Indexer()
ROBOTS_TXT_HANDLER = RobotsTxtHandler(USER_AGENT)
SCHEDULER = Scheduler(URL_FRONTIER, DOWNLOADER_POOL, PARSER_POOL, INDEXER, ROBOTS_TXT_HANDLER)

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
    respect_robots_txt = sys.argv[3] == '1'
    SCHEDULER.crawl(seed_url, depth=depth)
    # # SCHEDULER.crawl(seed_url, depth, respect_robots_txt, progress_callback=print_progress, result_callback=print_result)
    # URL_FRONTIER.add_url(seed_url)
    # while URL_FRONTIER.has_next():
    #     nxt_url = URL_FRONTIER.get_next_url() 
    #     x = DOWNLOADER_POOL[0].fetch(nxt_url)
    #     txt,links,metadata = PARSER_POOL[0].parse(x,nxt_url)
    #     INDEXER.index(nxt_url,txt,links)
    # for i in INDEXER.text_index:
    #     print(i)
    #     # print(INDEXER.url_index)