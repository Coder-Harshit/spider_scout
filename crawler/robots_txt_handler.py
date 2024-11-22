import requests
from urllib.parse import urlparse

class RobotsTxtHandler:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.rules = {}

    def fetch_robots_txt(self, url):
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        try:
            response = requests.get(robots_url, headers={'User-Agent': self.user_agent})
            if response.status_code == 200:
                self.parse_robots_txt(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Error Fetching robots.txt: {err}")

    def parse_robots_txt(self, robots_txt):
        lines = robots_txt.splitlines()
        current_user_agent = None
        for line in lines:
            line = line.strip()
            if line.startswith('User-agent:'):
                current_user_agent = line.split(':')[1].strip()
            elif line.startswith('Disallow:') and current_user_agent == self.user_agent:
                path = line.split(':')[1].strip()
                self.rules[path] = 'disallow'
            elif line.startswith('Allow:') and current_user_agent == self.user_agent:
                path = line.split(':')[1].strip()
                self.rules[path] = 'allow'

    def is_allowed(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        for rule, action in self.rules.items():
            if path.startswith(rule):
                return action == 'allow'
        return True