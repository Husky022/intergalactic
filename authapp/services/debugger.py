from functools import wraps
from time import time


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'{func.__name__} time: {end - start}')
        return result
    return wrapper