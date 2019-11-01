#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from readCSV import getIdIter
from worker import workjob

'''
conda activate kinetics
python download.py data/kinetics-400_test.csv k400
python download.py data/kinetics-400_train.csv k400
python download.py data/kinetics-400_val.csv k400

download one:
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ
you-get -i https://www.youtube.com/watch?v=--6bJUbfpnQ

youtube-dl --skip-download https://www.youtube.com/watch?v=-gw9DlQGiNo

'''

def readSet(filename):
    file = open(filename,'r')
    badlist = file.readlines()
    badlist = [i.rstrip('\n') for i in badlist]
    bad = set(badlist)
    return bad

def theIter(input_csv): 
    #bad set
    badfile = 'bad_video.log'
    badset = readSet(badfile)   
    #downloaded
    dedfile1 = 'exist.txt'
    dedset1 = readSet(dedfile1)
    dedfile3 = 'bdnet.txt'
    dedset3 = readSet(dedfile3)
    
    #video list    
    for item in getIdIter(input_csv):
        if item in badset:
            continue
        if item in dedset1:
            continue
        if item in dedset3:
            continue
        yield item


def main(input_csv, output_dir,num_jobs):
    # print(input_csv)
    # print(output_dir)
    # print(num_jobs)
    for i in theIter(input_csv):    
        workjob(i,output_dir)
        

if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_csv',type=str,help=('CSV file containing the following format: '
            'YouTube Identifier,Start time,End time,Class label'    ) ) 
    p.add_argument('output_dir',type=str,
        help=('Output directory where videos will be saved.') ) 
    p.add_argument('-n', '--num-jobs', type=int, default=3)

    main(**vars(p.parse_args() ) )
	
