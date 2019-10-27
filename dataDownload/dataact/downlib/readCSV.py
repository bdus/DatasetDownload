#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os

'''

'''

def readCSV(input_csv ):    
    """
    arguments:
    ---------
    input_csv: str
        Path to CSV file containing the following columns:
          'YouTube Identifier,Start time,End time,Class label'

    returns:
    -------
    dataset: DataFrame
        Pandas with the following columns:
            'video-id', 'start-time', 'end-time', 'label-name'
	"""
    #print(input_csv)
    df = pd.read_csv(input_csv)
    return df

def readCSVSet(input_csv):
    df = readCSV(input_csv)
    return set(df['youtube_id'])

def getIdIter(input_csv):
    df = readCSV(input_csv)
    for item in df['youtube_id']:
        yield item

if __name__ == '__main__':
    fpath = '/home/bdus/lcx/Action-Recognition/dataDownload/Kinetics/data'
    filename = 'kinetics-400_test.csv'
    filepath = os.path.join(fpath,filename)
    df = None
    if os.path.exists(filepath) == True:
        df = readCSV(filepath)
    #print(df)
    # cnt = 0    
    # for i in df['youtube_id']:
        # cnt += 1
        # if cnt > 10:
            # break
        # print(i)
    cnt = 0
    for i in getIdIter(filepath):
        cnt += 1
        if cnt > 10:
            break
        print(i)
