#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()


def wrap_requests(method: Callable) -> Callable:
    """ Decorator wrapper """
    @wraps(fn)
    def wrapper(url) -> str:
        """ Wrapper for decorator guy """
        r.incr(f'count:{url}')
        result = r.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """get page
    """
    return requests.get(url).text
