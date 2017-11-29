from .item import Item
import asyncio

class Crawler(object):
    """
    base class of each crawler
    """

    def __init__(self):
        pass

    async def persist_async(self, item):
        await asyncio.sleep(1)
        print('An item is persisted, {} bytes'.format(len(item.content)))

    def persist(self, item):
        print('An item is persisted, {} bytes'.format(len(item.content)))

    def start_requests(self):
        pass
