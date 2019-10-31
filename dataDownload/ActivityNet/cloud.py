#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:30:54 2019

@author: hp
"""

import argparse
import os

from lib.JsonLoader import readJsonSet
from lib.readCSV import readCSVSet
from lib.readTXT import readTXTSet
from lib.worker import workjob

'''
conda activate videodl

python cloud.py data/ActivityNet-200/activity_net.v1-3.min.json json act200
python cloud.py data/ActivityNet-100/activity_net.v1-2.min.json json act100
'''

def readSet(input_file,fmt):
    if fmt == 'json':
        dataset = readJsonSet(input_file)
    elif fmt == 'txt':
        dataset = readTXTSet(input_file)
    elif fmt == 'csv':
        dataset = readCSVSet(input_file)
    else:
        return {}
    return dataset

def setOp(dataset): 
    #bad set
    #badfiles = ['bad_video.log','act100.txt','bdnet.txt']
    badfiles = ['bad_video.log','act100.txt','bdnet.txt']
    badset = set()
    for badfile in badfiles:
        if os.path.exists(badfile) == True:
            tmpset = readTXTSet(badfile)
            badset = set.union(badset,set(tmpset))

    #video list    
    return set.difference(set(dataset),badset)
    

def main(args):
#    print args.input_file
#    print args.output_dir
#    print args.fmt
#    print(args.input_file)
#    print( args.output_dir)
#    print( args.fmt)
    dataset = readSet(args.input_file,args.fmt)
    for i in setOp(dataset):
        #workjob(i,output_dir)
        print(i)
    

if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_file',type=str, help=('input file name')) 
    p.add_argument('fmt',type=str,default='json',choices=['json','txt','csv'],help=('Input file format') ) 
    p.add_argument('output_dir',type=str, help=('Output directory where videos will be saved.') ) 
    #p.add_argument('-n', '--num-jobs', type=int, default=2)
    #main(**vars(p.parse_args() ) )
    main( p.parse_args() )
	
