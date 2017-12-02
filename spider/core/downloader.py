import aiohttp
import asyncio
from .event_manager import event_manager, Events
from ..utils.log_decorator import log
from ..middleware.user_agent_mw import UserAgentMiddleware
import time
import logging

class Downloader(object):
    def __init__(self, crawler, loop):
        self.crawler = crawler
        self.mw = []
        self._loop = loop
        self.subscribe()
        self.add_middlewarecls(UserAgentMiddleware, 1)

    def subscribe(self):
        event_manager.AddEventListener(Events.ENGINE_START, self.open)
        event_manager.AddEventListener(Events.ENGINE_CLOSE, self.close)

    @log(start='downloader start')
    def open(self):
        self._session = aiohttp.ClientSession(loop=self._loop, headers={ "Accept-Encoding": "gzip"})

    @log(end='downloader stop')
    def close(self):
        try:
            if not self._session.closed:
                self._session.close()
        except Exception as e:
            print(e)

    def add_middlewarecls(self, mw, pri):
        idx = 0
        while idx < len(self.mw) and pri > mw[idx][1]:
            idx += 1
        self.mw.insert(idx, (mw, pri))

    def apply_middlewares(self, request):
        for mwcls, pri in self.mw:
            mw = mwcls()
            mw.process_request(request)

    async def start_download(self, request):
        try:
            start = time.time()
            response = await self._session.get(request.url, timeout=10)
            content = await response.text()
            await response.release()
            end = time.time()
            logging.debug('{} downloaded, spent {}, {} bytes.'.format(request.url, end - start, len(content)))
            return content
        except:
            logging.warning('download {} failed.'.format(request.url))

    async def do_download(self, request):
        self.apply_middlewares(request)
        return await self.start_download(request)
