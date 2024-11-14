from bs4 import BeautifulSoup
import re
import logging

class Parser:
    def __init__(self):
        self.state = 'idle'
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialized Parser")

    def parse(self, html_content, root_url):
        try:
            self.logger.info(f"Parsing HTML content")
            soup = BeautifulSoup(html_content, 'html.parser')
            textual_content = soup.get_text()
            links = set()

            for link in soup.find_all('a'):
                # in all anchor tags
                href = link.get('href')
                if href:
                    if re.search("^http",href):
                        links.add(href.rstrip("/"))
                    else:
                        links.add((root_url+href).rstrip("/"))
            
            # metadata
            title = soup.title.text if soup.title else None
            
            desc_tag = soup.find('meta', attrs={'name':'description'})
            desc = desc_tag['content'] if desc_tag else None
            
            metadata = {
                'title':title,
                'description':desc
            }

            # #####
            # print(f"Extracted text: {textual_content}", file=open('spiderscout.log', 'a'))
            # print(f"Extracted links: {links}", file=open('spiderscout.log', 'a'))
            # print(f"Extracted metadata: {metadata}", file=open('spiderscout.log', 'a'))
            # #######################################

            return textual_content, links, metadata

        except Exception as e:
            self.logger.error(f"Error parsing HTML content: {str(e)}", exc_info=True)
