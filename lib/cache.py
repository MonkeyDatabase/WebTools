from functools import wraps
from typing import Callable, Coroutine, Union
from lib.utils import gen_md5
import os
import json


class FileCache:
    def __init__(self, cls: any = None):
        self.raw = cls
        if not os.path.exists('cache/'):
            os.mkdir('cache')

    def __getitem__(self, key: str)->Union[bytes, None]:
        key = key.encode()
        md5 = gen_md5(key)
        if self.raw:
            self.raw.raw_html = md5
        path = f'cache/{md5}'
        if os.path.exists(path):
            with open(path, 'rb+') as f:
                return f.read()
        else:
            return None

    def __setitem__(self, key: str, value: bytes):
        key = key.encode()
        md5 = gen_md5(key)
        path = f'cache/{md5}'
        with open(path, 'wb+') as f:
            f.write(value)


def a_cached(func: Coroutine):
    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        filecache = FileCache(cls)
        key_parts = [func.__name__] + list(args)
        key = json.dumps(key_parts)
        result = filecache[key]
        if result:
            value = result
        else:
            value = await func(cls, *args, **kwargs)
            filecache[key] = value
        return value
    return wrapper


def cached(func: Callable):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        filecache = FileCache(cls)
        key_parts = [func.__name__] + list(args)
        key = json.dumps(key_parts)
        result = filecache[key]
        if result:
            value = result
        else:
            value = func(cls, *args, **kwargs)
            filecache[key] = value
        return value
    return wrapper

