class Request(object):
    def __init__(self, url, param=None, header=None, body=None, callback=None, data=None):
        self.url = url
        self.param = param or dict()
        self.header = header or dict()
        self.body = body
        self.callback = callback
        self.data = data or dict()
        self.depth = 1
