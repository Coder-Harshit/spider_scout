from modules import frontier, parser, downloader, indexer, scheduler

N: int = 3

DOWNLOADER_POOL = [downloader.Downloader(user_agent='spider_scout/1.0 (+mailto:21803015@mail.jiit.ac.in)') for _ in range(N)]
PARSER_POOL = [parser.Parser() for _ in range(N)]

url_frontier = frontier.URLFrontier()
indexer = indexer.Indexer()
scheduler = scheduler.Scheduler(url_frontier, DOWNLOADER_POOL, PARSER_POOL, indexer)

scheduler.crawl("https://www.archwiki.org",depth=2)

print("\n------TEXT_INDEX------")
for (key,value) in indexer.text_index.items():
    print(key, " : ", value)


print("\n\n\n------URL_INDEX------")
for (key,value) in indexer.url_index.items():
    print(key, " : ", value)