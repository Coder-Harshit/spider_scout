# SPIDERSCOUT

## Module Planning
### URL Frontier Module
Responsible for managing & selection of the URLs (for crawlling)

### Downloader Module
To download the web page as per the politeness policies

### Parser Module
Parses the HTML content and extract the metadata, images, links etc. from the downloaded content

### Indexer Module
Responsible for maintaining the inverted index of the retrieved/extracted data

### Scheduler Module
`Manager`, coordinates the overall crwalling process and assigning tasks to various modules.