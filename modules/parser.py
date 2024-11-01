from bs4 import BeautifulSoup

class Parser:
    def parse(self, html_content):
        #######################################
        # logging
        print(f"Parsing HTML content:", file=open('spiderscout.log', 'a'))
        #####

        soup = BeautifulSoup(html_content, 'html.parser')

        textual_content = soup.get_text()

        links = []
        for link in soup.find_all('a'):
            # in all anchor tags
            href = link.get('href')
            if href:
                links.append(href)
        
        # metadata
        title = soup.title.text if soup.title else None
        
        desc_tag = soup.find('meta', attrs={'name':'description'})
        desc = desc_tag['content'] if desc_tag else None
        
        metadata = {
            'title':title,
            'description':desc
        }

        #####
        print(f"Extracted text: {textual_content}", file=open('spiderscout.log', 'a'))
        print(f"Extracted links: {links}", file=open('spiderscout.log', 'a'))
        print(f"Extracted metadata: {metadata}", file=open('spiderscout.log', 'a'))
        #######################################

        return textual_content, links, metadata