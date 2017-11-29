from enum import Enum
from collections import defaultdict

class Events(Enum):
    ENGINE_START = 'ENGINE_START'
    ENGINE_CLOSE = 'ENGINE_CLOSE'


class EventType(Enum):
    Once = 'Once'
    Forever = 'Forever'


class EventHandler(object):
    def __init__(self, etype, handler):
        self.etype = etype
        self.handler = handler


class EventManager(object):
    '''
    Event manager, provide event-driven. Singleton.
    '''
    def __init__(self):
        self._handler = defaultdict(dict)

    def AddEventListener(self, ename, handler, etype=EventType.Forever):
        hdict = self._handler[ename]
        if handler not in hdict.keys():
            hdict[handler] = etype

    def RemoveEventListener(self, ename, handler):
        hdict = self._handler[ename]
        if handler in hdict.keys():
            del hdict[handler]

    def SendEvent(self, ename, *args, **kwargs):
        hdict = self._handler[ename]
        todelete = []
        for handler in hdict.keys():
            if hdict[handler] == EventType.Once:
                todelete.append(handler)
            handler(*args, **kwargs)
        # delete events that only subscribe once
        for h in todelete:
            del hdict[h]

event_manager = EventManager()
