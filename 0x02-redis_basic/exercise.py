#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage.
"""
import redis
import uuid
from typing import Union


class Cache:
    """Represents an object for storing data in a
    Redis data storage.
    """
    def __init__(self):
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
