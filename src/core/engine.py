import asyncio
from scheduler import Scheduler
from downloader import Downloader
from itembase import Item


class Engine(object):
    '''
    this is the engine of all components
    '''
    def __init__(self, crawler ,arg):
        self.crawler = crawler
        self.scheduler = Scheduler(crawler)
        self.downloader = Downloader(crawler)

    def start_engine(self):
        '''
        starting point of whole system
        '''
        pass

    async def work(self):
        for req in self.crawler.start_requests():
            self.scheduler.schedule(req)

        while True:
            request = self._next_request_from_scheduler()
            if not request:
                break
            content = await self._download(request)
            for item in request.callback(content):
                assert isinstance(item, (Request, Item)), "unexpected type"
                if isinstance(item, Item):
                    await self.crawler.persist(item)
                else:
                    self.scheduler.schedule(item)

    def _next_request_from_scheduler(self):
        return self.scheduler.next_request()

    async def _download(self, request):
        return await self.downloader.do_download(request)
