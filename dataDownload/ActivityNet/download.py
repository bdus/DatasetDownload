import argparse
import os
import subprocess

from JsonLoader import urlkeyIter
from worker import download_job

from joblib import delayed
from joblib import Parallel

'''
conda activate videodl

python download.py ActivityNet-200/activity_net.v1-3.min.json ActivityNet-200
'''

def notbadIter(input_json): 
    #bad set
    file = open('bad_video.log','r')
    badlist = file.readlines()
    badlist = [i.rstrip('\n') for i in badlist]
    bad = set(badlist)
    #video list    
    for item in urlkeyIter(input_json):
        if item in bad:
            continue
        yield item
    

def main(input_json, output_dir,num_jobs):
    # print(input_json)
    # print(output_dir)
    # print(num_jobs)    
    Parallel(n_jobs=num_jobs)(delayed(download_job)(i,output_dir) for i in notbadIter(input_json))
    # file = open('bad_video.log','r')
    # badlist = file.readlines()
    # badlist = [i.rstrip('\n') for i in badlist]
    # bad = set(badlist)
    # cnt = 2
    # for i in urlkeyIter(input_json):
    #     cnt += 1
    #     if cnt > 10:
    #         break
    #     if i in bad:            
    #         continue		
    #     download_job(i,output_dir)

if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_json',type=str, help=('ActivityNet Json file') ) 
    p.add_argument('output_dir',type=str, help=('Output directory where videos will be saved.') ) 
    p.add_argument('-n', '--num-jobs', type=int, default=2)

    main(**vars(p.parse_args() ) )
	