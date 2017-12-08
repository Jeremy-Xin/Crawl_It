import logging
import os
from ..utils.config_loader import get_config

class Logger:
    # logging.basicConfig(level=numeric_level)
    # logging.basicConfig(format='%(asctime)s-%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def __init__(self):
        self.mlogger = logging.getLogger('spider')
        self.init_logger()

    def init_logger(self):
        config = get_config() or dict()
        loglevel = config.get('spider_log_level', 'debug')
        numeric_level = getattr(logging, loglevel.upper(), None)
        self.mlogger.setLevel(numeric_level)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.mlogger.addHandler(ch)

logger = Logger().mlogger

def set_level(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    logger.setLevel(numeric_level)
