#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import subprocess
from bypy import ByPy, const
import youtube_dl

'''
python doanload3.py data/kinetics-400_test.csv download
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ

'''

#def download_job(youtube_id,
#	num_attempts=1,
#    url_base='https://www.youtube.com/watch?v='):  
#    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )
#    
#    command = ['youtube-dl',               
#               '-f', 'mp4',
#               '-o', path,
#               '"%s"' % (url_base + youtube_id)]
#    command = ' '.join(command)
#    print command
#    attempts = 0
#    while True:
#        try:
#            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
#        except subprocess.CalledProcessError as err:
#            print youtube_id + ' is bad.'
##            print(youtube_id)
#            fo = open("bad_video.log","a")
#            fo.write(youtube_id)
#            fo.write("\n")
#            fo.close()
#            attempts += 1
#            if attempts == num_attempts:
#                return False#status, err.output
#            else:
#                break

def download(youtube_id):    
    url_base='https://www.youtube.com/watch?v='
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )
    download_url = '%s' % (url_base + youtube_id)
    ydl_opts = {
        # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存 http://www.yujzw.com/python/python-youtube-dl.html
        'format' : 'best', 
        'quiet' : True,
        'outtmpl': u'tmp/%(id)s.%(ext)s'
    }
    try:
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        print 'downloading ',youtube_id
        ydl.download([download_url])
    except youtube_dl.utils.DownloadError,err:
        print 'ydl error! Add to bad_video list.'
        for arg in err.args:
            print arg
        fo = open("bad_video.log","a")
        fo.write(youtube_id)
        fo.write("\n")
        fo.close()   


def chkok(by, result):
    ans = True
    if by.processes == 1:
        if result != const.ENoError and result != const.EHashMismatch:
            print "Failed, result: {}".format(result)
            print bp.response.json()
            ans = False
    else:
        if result != const.ENoError and result != const.IEFileAlreadyExists and result != const.EHashMismatch:
            print "Failed, result: {}".format(result)
            print bp.response.json()
            ans = False
    return ans

def upload_job(youtube_id,path_bdnet):
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )
    bp =  ByPy()
    try:
        print 'download ok. uploading.'
        ans = bp.upload(localpath=path, remotepath=path_bdnet, ondup=u'overwrite')
        resp = chkok(bp,ans)
        print 'ans:'+str(ans)+';'
        if os.path.exists(path):
            with open('bdnet.txt',"a") as fo:
                fo.write(youtube_id)
                fo.write("\n")
                fo.close()
    except Exception,e:
        print 'upload failed.'
        print bp.response.json()
        print e        

def del_job(youtube_id):
    path = os.path.join('tmp' ,''.join([youtube_id,".mp4"]) )    
    if os.path.exists(path):        
        os.remove(path)
        print 'file exist. deleted'

def workjob(youtubeid,path):
    download(youtubeid)
    tmppath = os.path.join('tmp' ,''.join([youtubeid,".mp4"]) )
    if os.path.exists(tmppath) == True:
        upload_job(youtubeid,path)
        del_job(youtubeid)

if __name__ == '__main__':
    path = 'tmp'
    youtubeid = '--6bJUbfpnQ'
    badid = 'x99PS_O6JW8'
    workjob(youtubeid,path)
    #download(badid)
