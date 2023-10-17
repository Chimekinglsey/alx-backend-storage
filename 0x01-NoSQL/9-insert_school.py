#!/usr/bin/env python3
""" 9-insert_school.py """


def insert_school(mongo_collection, **kwargs):
    """ insert a new document to collection and return _id"""
    contents = {}
    for k,v in kwargs.items():
        contents.update({k: v})
    insert_value = mongo_collection.insert_one(contents)
    return insert_value.inserted_id