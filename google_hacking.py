from __future__ import unicode_literals
import json
import re
from mixins.attrdict import AttrDict
from constant.constant import GoogleHackingConstant as Constant
from spider.googlespider import GoogleSpider
from typing import List


class Google_Hacking(AttrDict):
    __exclude_keys__ = {'_Google_Hacking__dork_spiders', 'target', 'dorks'}

    def __init__(self, url, pages=1, offset=0, time_window='a'):
        self.url = url
        self.target = re.split("\.", url)[0]
        self.dorks = []

        self.pages = pages
        self.offset = offset
        self.time_window = time_window

        self.__dork_spiders: List = []

        self.main: dict = {}
        self.wiki: dict = {}
        self.news: dict = {}

        if (self.time_window[0] not in ('a', 'd', 'h', 'm', 'n', 'w', 'y')) or (len(self.time_window) > 1 and not self.time_window[1:].isdigit()):
            print("invalid time interval specified.")
            self.time_window = 'a'

    def __generate_dorks(self):
        print(f'\033[1;33m[GOOGLE_HACKING] generating dorks\033[0m')
        for dork_name, dork_format in Constant.dork_formats.items():
            dork_name = re.sub("\(.*\)", "", dork_name)
            dork_value = re.sub("\$target", self.target, dork_format)
            dork_value = re.sub("\$domain", self.url, dork_value)
            # dork_value = re.sub(r'%20', '+', dork_value)
            # dork_value = re.sub(r'"|\"', '%22', dork_value)
            self.dorks.append({
                "name": dork_name,
                "url": dork_value
            })
        print(f'\033[1;33m[GOOGLE_HACKING] generated dorks successfully\033[0m')

    def __iterate_page(self, dork, page):
        if not dork:
            print(f"\033[1;33minvalid dork for {dork}\033[0m")
            return
        page_now = (self.offset * 10) + (page * 10)
        target_url = "https://google.com/search?start=%i&tbs=qdr:%s&q=%s&filter=0" % (page_now, self.time_window, dork['url'])

        google_spider = GoogleSpider(target_url)
        google_spider.search()
        self.__dork_spiders.append({
            "dork_name": dork['name'],
            "spider": google_spider
        })

    def __iterate_dork(self, dork: dict):
        for page in range(0, self.pages):
            self.__iterate_page(dork, page)

    def __iterate_dorks(self):
        print(f'\033[1;33m[GOOGLE_HACKING] __iterate_dorks started\033[0m')
        for dork in self.dorks:
            self.__iterate_dork(dork)
        print(f'\033[1;33m[GOOGLE_HACKING] __iterate_dorks finished successfully\033[0m')

    def __post_processing_item(self, item_name: str, item_list: list, dork_name: str):
        for item in item_list:
            if dork_name not in self[item_name].keys():
                self[item_name].update({
                    dork_name: []
                })
            if item not in self[item_name][dork_name]:
                self[item_name][dork_name].append(item)

    def __post_processing(self):
        print(f'\033[1;33m[GOOGLE_HACKING] __post_processing started\033[0m')
        for dork_spider in self.__dork_spiders:
            dork_name = dork_spider['dork_name']
            spider = dork_spider['spider']
            self.__post_processing_item('main', spider['main'], dork_name)
            self.__post_processing_item('news', spider['news'], dork_name)
            self.__post_processing_item('wiki', spider['wiki'], dork_name)
        print(f'\033[1;33m[GOOGLE_HACKING] __post_processing finished successfully\033[0m')

    def search(self):
        self.__generate_dorks()
        self.__iterate_dorks()
        self.__post_processing()


if __name__ == '__main__':
    google_hacking = Google_Hacking('bytedance.com', pages=5)
    google_hacking.search()

    print(json.dumps(dict(google_hacking), ensure_ascii=False, indent=2))
