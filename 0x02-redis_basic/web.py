#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """
    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator guy """
        r.incr(f"count:{url}")
        cached_response = r.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        r.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """get page
    """
    response = requests.get(url)
    return response.text
