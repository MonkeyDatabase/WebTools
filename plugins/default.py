from typing import Optional, Tuple
from lib.classtype import TypePlugin
from lib.cache import cached
import requests
from bs4 import BeautifulSoup

class Plugin(TypePlugin):
    priority = 5

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }
        self.raw_html = ''

    @cached
    def __get_source(self, url: str, headers: dict) -> bytes:
        page = requests.get(url=url, headers=headers, allow_redirects=False)
        return page.content

    def get_source(self, url: Optional[str] = None) -> Tuple[BeautifulSoup, str]:
        """get the source of target url
        :param url: target url
        :return: beautifulsoup of the source and the source
        """
        if not url:
            raise Exception
        self.raw_html = self.__get_source(url, self.headers).decode('utf-8')
        return BeautifulSoup(self.raw_html, 'html.parser'), self.raw_html

