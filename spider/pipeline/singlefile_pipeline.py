from ..base.pipeline import Pipeline

class SingleFilePipeline(Pipeline):
    def __init__(self):
        self.open()
        self.num = 0

    def subscribe(self):
        pass

    def open(self):
        self.f = open('test.txt', 'w')

    def close(self):
        pass

    async def process_item(self, item):
        self.num += 1
        # print('processing item {}'.format(self.num))
        self.f.write(item.content)
        self.f.write('\n')
