#!/usr/bin/env python3
"""Using ODM for mongodb"""
import mongoengine, pymongo


def list_all(mongo_collection):
    """A function that lists all docs in a collection"""
    if mongo_collection is not None:
        return mongo_collection.find()
    return []