from asyncio import Queue
import asyncio
import time
import datetime

class Scheduler(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.requests = Queue(maxsize=1024)
        self.crawled = set()

    async def next_request(self):
        # await asyncio.sleep(1)
        r = await self.requests.get()
        return r

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
        # print(self.requests.empty)
        # endtime = datetime.datetime.now() + datetime.timedelta(seconds=10)
        # while datetime.datetime.now() < endtime:
        #     if not self.requests.empty():
        #         return True
        #     else:
        #         time.sleep(1)
        # return False
