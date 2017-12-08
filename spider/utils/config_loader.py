import logging

config = None

def from_object(myconfig):
    global config
    config = myconfig


def from_file(path):
    pass


def get_config():
    return config
