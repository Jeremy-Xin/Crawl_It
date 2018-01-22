import sys
sys.path.insert(1, '..')

from spider.core.engine import Engine
from spider.base.crawler import Crawler
from spider.http.request import Request
from spider.base.item import Item
from spider.parser.html_parser import HtmlParser
import re
import bs4
from bs4 import BeautifulSoup
import time
import logging
import logging.config
from spider.utils import config_loader
import config

class MockCrawler(Crawler):
    detail_pattern = 'detail/index/soft_id/'
    crawled = set()
    base_url = 'http://zhushou.360.cn'
    start_url = ['http://zhushou.360.cn/game/', 'http://zhushou.360.cn/soft']
    # start_url = ['https://www.zhihu.com/']


    def start_requests(self):
        for url in self.start_url:
            self.crawled.add(url)
            yield Request(url, callback=self.process_links)

    def process_links(self, response):
        start = time.time()
        content = response.content
        request = response.request
        links = HtmlParser().extract_link(content, base_url=request.url)
        # print('{} has {} links'.format(request.url, len(links)))
        for link in links:
            # app
            if re.search(self.detail_pattern, link):
                if not link in self.crawled:
                    self.crawled.add(link)
                    yield Request(link, callback=self.process_item)
            # other pages
            elif link.startswith(self.base_url):
                if not link in self.crawled:
                    self.crawled.add(link)
                    yield Request(link, callback=self.process_links)
        end = time.time()
        # print('Process_links spent {}'.format(end - start))

    def process_item(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        app_name = soup.select('h2#app-name span')
        if len(app_name):
            yield Item(app_name[0].text)

# config = {'spider_log_level':'info'}
config_dict = config_loader.from_file(config)
# config_loader.from_file('logging.conf')
e = Engine(MockCrawler(), config_dict)
e.start_engine()
