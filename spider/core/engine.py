import asyncio
from .scheduler import Scheduler
from .downloader import Downloader
from ..base.item import Item
from .event_manager import event_manager, Events
from ..http.request import Request
from ..http.response import Response
from ..utils.log_decorator import log
import traceback
from ..pipeline.singlefile_pipeline import SingleFilePipeline
from ..utils import config_loader
from ..utils import logger_util
from ..utils import logger

class Engine(object):
    '''
    this is the engine of all components
    '''
    def __init__(self, crawler, config, loop=None, ):
        self.crawler = crawler
        self.scheduler = Scheduler(crawler)
        self.downloader = Downloader(crawler, loop)
        self.running_tasks = []
        self.parallel_num = 8
        self._loop = loop or asyncio.get_event_loop()
        self.started = False
        self.pipeline = SingleFilePipeline()
        self.max_depth = 5
        config_loader.from_object(config)
        logger_util.set_level(config['spider_log_level'])

    def start_engine(self):
        '''
        starting point of whole system
        '''
        try:
            # asyncio.Task(self.start())
            # self._loop.run_forever()
            self._loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            print('keyboard interrupt')
            for task in self.running_tasks:
                task.cancel()
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

        self.running_tasks = [asyncio.Task(self.do_works(i + 1)) for i in range(self.parallel_num)]
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
        try:
            idle_round = 0
            while True:
                if self.scheduler.have_next():
                    idle_round = 0
                    await self.do_one_work(idx)
                else:
                    await asyncio.sleep(1)
                    # print('sleep')
                    idle_round += 1
                    if idle_round > 10:
                        break
            logger.info('Worker{} Done!'.format(idx))
        except:
            logger.error('Worker {} got exception!'.format(idx))

    # async def do_works(self, idx):
    #     while True:
    #         await self.do_one_work(idx)

    async def do_one_work(self, idx):
        '''
        process one request in a coroutine
        '''
        request = await self._next_request_from_scheduler()
        if not request:
            return
        content = await self._download(request)
        if not content:
            return
        response = Response(content, request)
        for item in request.callback(response):
            assert isinstance(item, (Request, Item)), "unexpected type"
            if isinstance(item, Item):
                await self.pipeline.process_item(item)
            else:
                item.depth = request.depth + 1
                if item.depth > self.max_depth:
                    continue
                await self.scheduler.schedule(item)

    async def _next_request_from_scheduler(self):
        return await self.scheduler.next_request()

    async def _download(self, request):
        return await self.downloader.do_download(request)
