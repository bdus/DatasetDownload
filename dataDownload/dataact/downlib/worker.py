#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

'''
python doanload3.py data/kinetics-400_test.csv download
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ

'''

def download_job(youtube_id,
	num_attempts=1,
    url_base='https://www.youtube.com/watch?v='):  
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )
    
    command = ['youtube-dl',               
               '-f', 'mp4',
               '-o', path,
               '"%s"' % (url_base + youtube_id)]
    command = ' '.join(command)
    print command
    attempts = 0
    while True:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            print youtube_id + ' is bad.'
#            print(youtube_id)
            fo = open("bad_video.log","a")
            fo.write(youtube_id)
            fo.write("\n")
            fo.close()
            attempts += 1
            if attempts == num_attempts:
                return False#status, err.output
        else:
            break
    #os.system( ' '.join(command) )    

def upload_job(youtube_id,path_bdnet):
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )
    from bypy import ByPy     
    with ByPy() as bp:
        bp.upload(localpath=path, remotepath=path_bdnet, ondup=u'overwrite')
        

def del_job(youtube_id):
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )    
    if os.path.exists(path):
        with open('bdnet.txt',"a") as fo:
            fo.write(youtube_id)
            fo.write("\n")
            fo.close()
        os.remove(path)   

def workjob(youtubeid,path):
    download_job(youtubeid)
    tmppath = os.path.join('tmp' ,''.join([youtubeid,".mp4"]) )
    if os.path.exists(tmppath) == True:
        upload_job(youtubeid,path)
        del_job(youtubeid)

if __name__ == '__main__':
    path = 'tmp'
    youtubeid = 'E_sjapo5bS8'
    workjob(youtubeid,path)
