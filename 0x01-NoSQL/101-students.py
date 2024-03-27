#!/usr/bin/env python3
"""
Top students
"""


def top_students(mongo_collection):
    """Prints all students in a collection sorted by
    average score.
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
