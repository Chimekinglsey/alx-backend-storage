#!/usr/bin/env python3
"""  12. Log stats """
from pymongo import MongoClient


def log_stat(nginx_collection):
    """provides some stats about nginx logs stored in MongoDB"""
    print(f'{nginx_collection.count_documents({})} logs')
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = len(list(nginx_collection.find({'method': method})))
        print(f'\tmethod {method}: {count}')
    check_count_stat = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(check_count_stat))



def run():
    '''
    Initiates DB engine to provide stats
    '''
    client = MongoClient(host='localhost', port=27017)
    log_stat(client.logs.nginx)


if __name__ == '__main__':
    run()
