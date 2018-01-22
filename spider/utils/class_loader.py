import sys

def get_cls_from_name(name):
    last_dot_index = str(name).rfind('.')
    module_name = name[:last_dot_index]
    clazz_name = name[last_dot_index + 1:]
    __import__(module_name)
    module = sys.modules[module_name]
    clazz = getattr(module, clazz_name)
    return clazz