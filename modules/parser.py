from bs4 import BeautifulSoup

class Parser:
    def parse(self, html_content):
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
        
        metadata = {'title':title, 'description':desc}
        return textual_content, links, metadata