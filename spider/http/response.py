from .request import Request

class Response(object):
    def __init__(self, content, request):
        self.content = content
        self.request = request
