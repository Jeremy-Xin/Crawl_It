import aiohttp

class Downloader(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.mw = []
        x = (1,2)
        x.

    def add_middlewarecls(self, mw, pri):
        idx = 0
        while idx < len(self.mw) and pri > mw[idx][1]:
            idx += 1
        self.mw.insert(idx, (mw, pri))

    def apply_middlewares(self, request):
        for mwcls in self.mw:
            mw = mwcls()
            mw.process_request(request)

    async def start_download(self, request):
        pass

    async def do_download(self, request):
        apply_middlewares(request)
        await start_download(request)
