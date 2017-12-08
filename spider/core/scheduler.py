from asyncio import Queue
import asyncio
import time
import datetime
from ..utils import logger

class Scheduler(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.requests = Queue()
        self.crawled = set()

    async def next_request(self):
        # r = await self.requests.get()
        # return r
        return self.requests.get_nowait()

    def schedule_nowait(self, request):
        if not request.url in self.crawled:
            self.requests.put_nowait(request)
            self.crawled.add(request.url)

    async def schedule(self, request):
        if not request.url in self.crawled:
            await self.requests.put(request)
            self.crawled.add(request.url)

    def have_next(self):
        return not self.requests.empty()
