from modules import frontier, parser, downloader, indexer, scheduler
from modules.logger_config import setup_logger
import asyncio


logger = setup_logger()
logger.info("Starting Spider Scout crawler")


N: int = 5
USER_AGENT: str = 'spider_scout/1.0 (+mailto:21803015@mail.jiit.ac.in)' 
DOWNLOADER_POOL = [downloader.Downloader(user_agent=USER_AGENT) for _ in range(N)]
PARSER_POOL = [parser.Parser() for _ in range(N)]


url_frontier = frontier.URLFrontier()
indexer = indexer.Indexer()
scheduler = scheduler.Scheduler(url_frontier, DOWNLOADER_POOL, PARSER_POOL, indexer, USER_AGENT)

scheduler.crawl("https://www.archwiki.org",depth=1)
# scheduler.crawl("https://en.wikipedia.org/wiki/Jaypee_Institute_of_Information_Technology",depth=1)

# print("\n------TEXT_INDEX------")
# for (key,value) in indexer.text_index.items():
#     print(key, " : ", value)


# print("\n\n\n------URL_INDEX------")
# for (key,value) in indexer.url_index.items():
#     print(key, " : ", value)