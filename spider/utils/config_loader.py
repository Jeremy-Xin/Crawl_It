import logging
import types

config = {}
built_in = ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']


def from_object(myconfig):
    global config
    config = myconfig


def from_file(module):
    for entry in dir(module):
        if entry not in built_in:
            attr = getattr(module, entry)
            if not isinstance(attr, types.ModuleType):
                config[entry] = attr


def get_config():
    return config
