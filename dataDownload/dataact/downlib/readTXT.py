#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:04:15 2019

@author: bdus
@description: read a txt file by line into a set
"""
import os

def readTXTSet(filename):    
    file = open(filename,'r')
    records = file.readlines()
    records = [i.rstrip('\n') for i in records]
    records = set(records)
    return records
    

if __name__ == '__main__':
    file = '../act100.txt'
    if os.path.exists(file) == True:
        records = readTXTSet(file)
        print len(records)
        #print(len(records))
        tmp = records.pop()
        records.add(tmp)
        print tmp
        #print(tmp)
    
