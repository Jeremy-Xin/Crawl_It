import asyncio
from .scheduler import Scheduler
from .downloader import Downloader
from ..base.item import Item
from .event_manager import event_manager, Events
from ..http.request import Request
from ..http.response import Response
from ..utils.log_decorator import log
import traceback
from ..pipeline.singlefilepipeline import SingleFilePipeline

class Engine(object):
    '''
    this is the engine of all components
    '''
    def __init__(self, crawler, loop=None):
        self.crawler = crawler
        self.scheduler = Scheduler(crawler)
        self.downloader = Downloader(crawler, loop)
        self.running_tasks = []
        self.parallel_num = 10
        self._loop = loop or asyncio.get_event_loop()
        self.started = False
        self.pipeline = SingleFilePipeline()
        self.max_depth = 5

    def start_engine(self):
        '''
        starting point of whole system
        '''
        try:
            self._loop.run_until_complete(self.start())
        except Exception as ex:
            print(ex)
            traceback.print_tb(ex.__traceback__)
        finally:
            self._loop.stop()
            self._loop.close()
            event_manager.SendEvent(Events.ENGINE_CLOSE)
            print(len(self.crawler.crawled))
        return

    async def start(self):
        '''
        start several tasks to crawl
        '''
        event_manager.SendEvent(Events.ENGINE_START)
        self.init_crawler_request()

        self.running_tasks = [asyncio.Task(self.do_works(i + 1)) for i in range(64)]
        await asyncio.wait(self.running_tasks)

    def init_crawler_request(self):
        '''
        initialize the requests list from crawler
        '''
        for req in self.crawler.start_requests():
            self.scheduler.schedule_nowait(req)

    async def do_works(self, idx):
        '''
        deal with requests one by one
        '''
        idle_round = 0
        while True:
            if self.scheduler.have_next():
                await self.do_one_work()
            else:
                await asyncio.sleep(1)
                idle_round += 1
                if idle_round > 10:
                    break
        print('Worker{} Done!'.format(idx))

    async def do_one_work(self):
        '''
        process one request in a coroutine
        '''
        request = await self._next_request_from_scheduler()
        # if not request:
        #     break
        content = await self._download(request)
        response = Response(content, request)
        for item in request.callback(response):
            assert isinstance(item, (Request, Item)), "unexpected type"
            if isinstance(item, Item):
                await self.pipeline.process_item(item)
            else:
                item.depth = request.depth + 1
                if item.depth > self.max_depth:
                    return
                await self.scheduler.schedule(item)

    async def _next_request_from_scheduler(self):
        return await self.scheduler.next_request()

    async def _download(self, request):
        return await self.downloader.do_download(request)
