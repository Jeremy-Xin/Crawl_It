import logging
import sys

def log(start='', end='', stream=sys.stdout):
    def outer(func):
        def inner(*args, **kwargs):
            if start:
                stream.write(start + '\n')
            func(*args, **kwargs)
            if end:
                stream.write(end + '\n')
            stream.flush()
        return inner
    return outer


# tests
@log(start='start add')
def add(a, b):
    print('{} + {} = {}'.format(a, b, a + b))

@log(start='start mul', end='stop mul')
def mul(a, b):
    print('{} + {} = {}'.format(a, b, a * b))

if __name__ == '__main__':
    add(1, 2)
    mul(3, 4)
