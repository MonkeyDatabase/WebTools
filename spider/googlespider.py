import json
from bs4 import BeautifulSoup
from mixins.attrdict import AttrDict
from typing import List
import importlib


class GoogleSpider(AttrDict):
    __exclude_keys__ = {'soup', '_plugins', 'raw_html'}

    def __init__(self, url: str, plugins: List[str] = []):
        self.url = url
        self.soup = None
        self.raw_html = None

        self.main = []
        self.wiki = []
        self.news = []
        self.page_num = 0

        if len(plugins):
            self._plugins = [
                importlib.import_module(plugin, '.').Plugin() for plugin in plugins
            ]
        else:
            self._plugins = [importlib.import_module('plugins.default', '.').Plugin()]

    def __pre_process(self):
        for plugin in self._plugins:
            self.soup, self.raw_html = plugin.get_source(self.url)
            if self.soup:
                return
        exit('No Available Plugin can get the context of The target')

    def __search_main_body(self):
        """parse the title, url, description in the main body of the webpage
        """
        result_container = self.soup.findAll('div', class_='g')

        for container in result_container:
            try:
                title = container.find('h3').text
                url = container.find('a')['href']
                desc = container.find('div', class_='IsZvec').text
                self.main.append({
                    'title': title,
                    'url': url,
                    'desc': desc,
                    'type': 'result'
                })
            except Exception:
                continue

    def __search_wiki(self):
        """parse the content of wiki(the right side of the main webpage)
        """
        container = self.soup.find('div', class_='kp-wholepage')

        if container is None:
            return
        # title of the wiki
        title = container.find('h2', attrs={'data-attrid': 'title'}).find('span').text
        # subtitle of the wiki
        try:
            subtitle = container.find('div', attrs={'data-attrid': 'subtitle'}).text
        except AttributeError:
            subtitle = None
        # description of the target
        try:
            description = container.find('div', class_='kno-rdesc').find('span').text
        except AttributeError:
            description = None

        # url of the wiki
        try:
            url = container.find('div', class_='kno-rdesc').find('a')['href']
        except AttributeError:
            url = None

        try:
            table = []
            sections = container.findAll('div', class_='wp-ms')
            for section in sections:
                table_ = section.findAll('div', class_='rVusze')
                if len(table_) != 0:
                    table = table_
        except IndexError:
            table = []

        # several key-value information in wiki
        details = []
        for row in table:
            spans = row.findAll('span')

            details.append({
                'name': spans[0].text,
                'value': spans[1].text
            })
        self.wiki = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'url': url,
            'details': details,
            'type': 'wiki'
        }

    def __search_news(self):
        """deal with the news card, which usually occurs in chinese language mode
        """
        try:
            cards = self.soup.find('g-scrolling-carousel').findAll('g-inner-card')
            for card in cards:
                title = card.find('div', role='heading').text
                href = card.find('a')['href']
                self.news.append({
                    'title': title,
                    'href': href
                })
        except AttributeError:
            return

    def __get_total_page(self):
        """get the page number at the bottom of the webpage(which is usually not accurate)
        """
        pages_ = self.soup.find('span', id='xjs').findAll('td')
        page_num = 0
        for p in pages_:
            try:
                if int(p.text) > page_num:
                    page_num = int(p.text)
            except Exception:
                pass
        self.page_num = page_num

    def search(self):
        self.__pre_process()
        self.__search_main_body()
        self.__search_news()
        self.__search_wiki()
        self.__get_total_page()



if __name__ == '__main__':
    url = 'https://www.google.com/search?q=hackthebox'
    test = GoogleSpider(url, plugins=['plugins.headless'])
    test.search()
    print(dict(test))








