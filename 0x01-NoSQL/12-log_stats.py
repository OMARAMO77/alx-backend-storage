#!/usr/bin/env python3
""" 12. Log stats
"""


from pymongo import MongoClient


def log_stats():
    """ provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    total = nginx_collection.count_documents({})
    print(f"{total} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        res = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {res}")
    path = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{path} status check")


if __name__ == "__main__":
    log_stats()
