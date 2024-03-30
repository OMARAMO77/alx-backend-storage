#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


def log_stats():
    """ log_stats.
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
    print("IPs:")
    sorted_ips = nginx_collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print(f"\t{s.get('_id')}: {s.get('count')}")
        i += 1


if __name__ == "__main__":
    log_stats()
