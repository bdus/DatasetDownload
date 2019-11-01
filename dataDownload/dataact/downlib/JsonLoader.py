#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['getDataset']

import json
# json reader http://activity-net.org/download.html

def getDataset(filename):
    with open(filename,'r') as load_f: #with 是 python 异常捕获 try except finally 的美观写法
        load_dict = json.load(load_f)
        #assert load_dict['version'] == 'VERSION 1.2'
        database = load_dict['database']
        return database

def readJsonSet(filename):
    database = getDataset(filename)
    return set(database.keys())

def databaseIter(filename):
    database = getDataset(filename)
    for i in database.keys():
        yield database.get(i)

def urlIter(filename):
    database = getDataset(filename)
    for i in database.keys():
        yield database.get(i).get('url')

def urlkeyIter(filename):
    database = getDataset(filename)
    for i in database.keys():
        yield i


def main():
    filename = '../data/ActivityNet-100/activity_net.v1-2.min.json'
    cnt = 0
    for i in urlkeyIter(filename):
        if cnt < 2:
            cnt += 1
        else:
            break
        print(i)

if __name__ == '__main__':
    main()
    