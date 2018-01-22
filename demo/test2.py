import sys
sys.path.insert(1, '..')

import config
from spider.utils import config_loader

config_loader.from_file(config)
conf = config_loader.config

path = conf['scheduler_class']
last_dot_index = str(path).rfind('.')
module = path[:last_dot_index]
clazz = path[last_dot_index + 1:]
print(module)
print(clazz)

__import__(module)
m = sys.modules[module]
attr = getattr(m, clazz)
print(attr)