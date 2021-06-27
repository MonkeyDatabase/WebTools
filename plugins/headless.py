from typing import Optional, Tuple
from lib.classtype import TypePlugin
from lib.cache import a_cached
import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from bs4 import BeautifulSoup


class Plugin(TypePlugin):
    priority = 4

    def __init__(self):
        self.raw_html = ''

    @a_cached
    async def __get_source(self, url: str) -> bytes:
        browser = await launch(options={'headless': True, 'args': ['--no-sandbox']})
        page = await browser.newPage()
        await page.goto(url)
        try:
            await page.waitForSelector('.kp-wholepage', timeout=3000)
        except TimeoutError:
            print('[Headless] Time out.')

        # 该种方式获取到的content是str，需要转为bytes
        content = await page.content()
        content = content.encode()
        await browser.close()
        return content

    def get_source(self, url: Optional[str] = None) -> Tuple[BeautifulSoup, str]:
        if not url:
            raise Exception
        self.raw_html = asyncio.run(self.__get_source(url)).decode('utf-8')
        return BeautifulSoup(self.raw_html, 'html.parser'), self.raw_html
