#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:30:54 2019

@author: hp
"""

import argparse
import os

from JsonLoader import urlkeyIter
from worker import workjob
'''
conda activate videodl

python cloud.py ActivityNet-200/activity_net.v1-3.min.json act200
python cloud.py ActivityNet-100/activity_net.v1-3.min.json act100
'''
def readSet(filename):
    file = open(filename,'r')
    badlist = file.readlines()
    badlist = [i.rstrip('\n') for i in badlist]
    bad = set(badlist)
    return bad

def theIter(input_json): 
    #bad set
    badfile = 'bad_video.log'
    badset = readSet(badfile)   
    #downloaded
    dedfile1 = 'act100.txt'
    dedset1 = readSet(dedfile1)
    dedfile2 = 'act200.txt'
    dedset2 = readSet(dedfile2)
    dedfile3 = 'bdnet.txt'
    dedset3 = readSet(dedfile3)
    
    #video list    
    for item in urlkeyIter(input_json):
        if item in badset:
            continue
        if item in dedset1:
            continue
        if item in dedset2:
            continue
        if item in dedset3:
            continue
        yield item

def main(input_json, output_dir,num_jobs):
    # print(input_json)
    # print(output_dir)
    # print(num_jobs)    
    cnt = 0
    for i in theIter(input_json):    
        workjob(i,output_dir)
    

if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_json',type=str, help=('ActivityNet Json file') ) 
    p.add_argument('output_dir',type=str, help=('Output directory where videos will be saved.') ) 
    p.add_argument('-n', '--num-jobs', type=int, default=2)

    main(**vars(p.parse_args() ) )
	