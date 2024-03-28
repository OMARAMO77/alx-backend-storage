#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import requests
import redis


def get_page(url: str) -> str:
    """get page
    """
    r = redis.Redis()
    r.incr(f"count:{url}")

    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    r.setex(url, 10, page_content)
    return page_content
