import sys
import json
from modules import frontier, parser, downloader, indexer, scheduler
# from modules.logger_config import setup_logger
import asyncio


# logger = setup_logger()
# logger.info("Starting Spider Scout crawler")


N: int = 5
USER_AGENT: str = 'spider_scout/1.0 (+mailto:21803015@mail.jiit.ac.in)' 
# DOWNLOADER_POOL = [downloader.Downloader(user_agent=USER_AGENT) for _ in range(N)]
# PARSER_POOL = [parser.Parser() for _ in range(N)]


url_frontier = frontier.URLFrontier()
indexer = indexer.Indexer()
downloader = downloader.Downloader()
parser = parser.Parser()
# scheduler = scheduler.Scheduler(url_frontier, DOWNLOADER_POOL, PARSER_POOL, indexer, USER_AGENT)
scheduler = scheduler.Scheduler(url_frontier, downloader, parser, indexer, USER_AGENT)

def print_progress(progress):
    print(json.dumps({"type": "progress", "value": progress}), flush=True)

def print_result(url):
    print(json.dumps({"type": "result", "url": url}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py `<url>` `<depth>` <respect_robots_txt>")
        sys.exit(1)
    else:
        url = sys.argv[1]
        depth = int(sys.argv[2])
        respect_robots_txt = sys.argv[3] == '1'
        print(f"==>URL: {url}")
        print(f"==>DEPTH: {depth}")
        scheduler.crawl(url, depth=depth, respect_robots_txt=respect_robots_txt, progress_callback=print_progress, result_callback=print_result)