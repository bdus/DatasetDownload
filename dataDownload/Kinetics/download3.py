import argparse
import os
import subprocess

from downloader.readCSV import getIdIter
from downloader.worker import download_job

from joblib import delayed
from joblib import Parallel

'''
cd G:\video_cls\downloadhere
conda activate kinetics
python download3.py data/kinetics-400_test.csv t400
python download3.py data/kinetics-400_train.csv tr400
python download3.py data/kinetics-400_val.csv v400

download one:
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ

'''


def main(input_csv, output_dir,num_jobs):
    # print(input_csv)
    # print(output_dir)
    # print(num_jobs)
    Parallel(n_jobs=num_jobs)(delayed(download_job)(i,output_dir) for i in getIdIter(input_csv))
    # cnt = 0
    # for i in getIdIter(input_csv):
        # cnt += 1
        # if cnt > 10:
            # break
        # download_job(i,output_dir)    

if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_csv',type=str,help=('CSV file containing the following format: '
            'YouTube Identifier,Start time,End time,Class label'    ) ) 
    p.add_argument('output_dir',type=str,
        help=('Output directory where videos will be saved.') ) 
    p.add_argument('-n', '--num-jobs', type=int, default=24)

    main(**vars(p.parse_args() ) )
	