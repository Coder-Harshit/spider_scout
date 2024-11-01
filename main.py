from modules import frontier, parser, downloader, indexer, scheduler

url_frontier = frontier.URLFrontier()
downloader = downloader.Downloader(user_agent='spider_scout')
parser = parser.Parser()
indexer = indexer.Indexer()
scheduler = scheduler.Scheduler(url_frontier, downloader, parser, indexer)
scheduler.crawl("https://www.archwiki.org")