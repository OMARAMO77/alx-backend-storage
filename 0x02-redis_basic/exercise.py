#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage.
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = '{}:inputs'.format(method.__qualname__)
        outputs_key = '{}:outputs'.format(method.__qualname__)

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)

        return output
    return wrapper


class Cache:
    """Represents an object for storing data in a
    Redis data storage.
    """
    def __init__(self):
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage.
        """
        if not self._redis.exists(key):
            return None
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, fn=lambda x: int(x))
