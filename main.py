from modules import frontier, parser, downloader, indexer, scheduler

DOWNLOADERS = []
PARSERS = []
SCHEDULERS = []


url_frontier = frontier.URLFrontier()
downloader = downloader.Downloader(user_agent='spider_scout')
parser = parser.Parser()
indexer = indexer.Indexer()
scheduler = scheduler.Scheduler(url_frontier, downloader, parser, indexer)
scheduler.crawl("https://www.archwiki.org",depth=2)

print("\n------TEXT_INDEX------")
for (key,value) in indexer.text_index.items():
    print(key, " : ", value)


print("\n\n\n------URL_INDEX------")
for (key,value) in indexer.url_index.items():
    print(key, " : ", value)