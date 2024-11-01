# SPIDERSCOUT

## Module Planning
### URL Frontier Module
Responsible for managing & selection of the URLs (for crawlling)

### Parser Module
To Parse the HTML content and extract the metadata, images, links etc.

### Downloader Module
To Download the parsed data as per the politeness policies

### Indexer Module
Responsible for maintaining the inverted index of the retrieved/extracted data

### Scheduler Module
`Manager`, coordinates the overall crwalling process and assigning tasks to various modules.