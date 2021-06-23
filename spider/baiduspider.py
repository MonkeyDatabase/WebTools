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
        result_container = self.soup.findAll('div', class_='result')

        for container in result_container:
            try:
                title = container.find('h3').text
                url = container.find('a')['href']
                desc = container.find('div', class_='c-abstract').text
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
        pass

    def __search_news(self):
        """deal with the news card, which usually occurs in chinese language mode
        """
        pass

    def __get_total_page(self):
        """get the page number at the bottom of the webpage(which is usually not accurate)
        """
        try:
            page_container = self.soup.find('div', id='page')
            pages_ = page_container.findAll('span', class_='pc')
            page_now = int(page_container.find('strong').find('span', class_='pc').text)
            self.page_now = page_now
            page_num = page_now
            for p in pages_:
                try:
                    if int(p.text) > page_num:
                        page_num = int(p.text)
                except Exception:
                    pass
            self.page_num = page_num
        except Exception:
            self.page_num = 0
            print('页码为异步渲染，获取失败')

    def search(self):
        self.__pre_process()
        self.__search_main_body()
        self.__search_news()
        self.__search_wiki()
        self.__get_total_page()



if __name__ == '__main__':
    url = 'https://www.baidu.com/s?wd=site:edu.cn'
    test = GoogleSpider(url)
    test.search()
    print(dict(test))








