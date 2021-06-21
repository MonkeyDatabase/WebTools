from bs4 import BeautifulSoup
from mixins.attrdict import AttrDict


class GoogleSpider(AttrDict):
    __exclude_keys__ = ('soup')

    def __init__(self, soup:BeautifulSoup):
        self.soup = soup
        self.results = []
        self.wikis = []
        self.videos = []
        self.news = []
        self.page_num = 0

    def search_result(self):
        """parse the title, url, description
        """
        result_container = self.soup.findAll('div', class_='g')

        for container in result_container:
            try:
                title = container.find('h3').text
                url = container.find('a')['href']
                desc = container.find('div', class_='IsZvec').text
                self.results.append({
                    'title': title,
                    'url': url,
                    'desc': desc,
                    'type': 'result'
                })
            except Exception:
                continue

    def search_wiki(self):
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
        self.wikis = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'url': url,
            'details': details,
            'type': 'wiki'
        }

    def get_total_page(self):
        pages_ = self.soup.find('span', id='xjs').findAll('td')
        page_num = 0
        for p in pages_:
            try:
                if int(p.text) > page_num:
                    page_num = int(p.text)
            except Exception:
                pass
        self.page_num = page_num


if __name__ == '__main__':
    with open('./test_cases/tectent.html', 'r', encoding='utf-8') as f:
        res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    spider = GoogleSpider(soup)
    spider.search_result()
    spider.search_wiki()
    spider.get_total_page()
    print(dict(spider))








