class Item(object):
    '''
    this is the base class for all pipeline items
    every self-defined item should be derived from this class
    '''
    def __init__(self, content):
        self.content = content
