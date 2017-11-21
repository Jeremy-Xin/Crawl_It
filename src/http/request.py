class Request(object):
    def __init__(self, url, method='GET', header=None, body=None, callback=None):
        self.url = url
        self.method = method
        self.header = header
        self.body = body
        self.callback = callback
