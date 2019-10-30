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
class TheParty(object):
    def __init__(self,remote_path,localDlDir='tmp'):
        self.url_base='https://www.youtube.com/watch?v='
        self.ext = "mp4"
        self.LDlDir = localDlDir
        self.RDir = remote_path
        self.bad_video = 'bad_video.log'
        self.uploaded_video = 'bdnet.txt'        
        self.outtmpl = os.path.join(self.LDlDir,'%(id)s.%(ext)s')
        self.ydl_opts = {
                # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存 http://www.yujzw.com/python/python-youtube-dl.html
                'format' : 'best', 
                'quiet' : True,
                'outtmpl': self.outtmpl#u'tmp/%(id)s.%(ext)s'
                }        
        self.processes = 1
        self.dlqueue = list()
        self.que_max = 20
        self._init()
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        self.bp = ByPy(processes=self.processes)
        self.bp.info()
        
    def _init(self):
        if not os.path.exists(self.LDlDir):
            os.mkdir(self.LDlDir)
        else:
            for item in os.listdir(self.LDlDir):
                file,_ = os.path.splitext(item)
                self.dlqueue.append(file)
        # http://stackoverflow.com/a/27320254/404271
        # https://github.com/houtianze/bypy/blob/75a810df2d60048d5406a42666359d51339dcfdd/bypy/bypy.py#L119
        self.processes = 1
        #OpenVZ failed install multiprocesses
        
            
    def _addID(self,youtube_id,filename):
        fo = open(filename,"a")
        fo.write(youtube_id)
        fo.write("\n")
        fo.close()
        
    def _ydl(self,youtube_id):        
        download_url = '%s' % (self.url_base + youtube_id)
        try:
            print 'downloading ',youtube_id
            self.ydl.download([download_url])
        except youtube_dl.utils.DownloadError,err:
            print 'ydl error! Add to bad_video list.'
            for arg in err.args:
                print arg
            self._addID(youtube_id,self.bad_video)
            
    def download(self,youtube_id):
        self._ydl(youtube_id)
        fpath = os.path.join(self.LDlDir,''.join([youtube_id,'.',self.ext]) )
        return os.path.exists(fpath)
    
    def _cloud_exist(self,youtube_id):
        lfpath = os.path.join(self.LDlDir,''.join([youtube_id,'.',self.ext]))
        rfpath = os.path.join(self.RDir,''.join([youtube_id,'.',self.ext]) )
        assert os.path.exists(fpath)        
        try:
            ans = self.bp.meta(rfpath)
            if 0 == ans:
                return True
            elif 31066 == ans:
                return False
            else:
                print self.bp.response.json()
                raise Exception,'baiduyun failed.'
        except Exception,e:
            print 'baiduyun failed.'
            print self.bp.response.json()
            print e 
            
    def _chkok(self,result):        
        ans = True
        if self.bp.processes == 1:
            if result != const.ENoError and result != const.EHashMismatch:
                print "Failed, result: {}".format(result)
                print self.bp.response.json()
                ans = False
        else:
            if result != const.ENoError and result != const.IEFileAlreadyExists and result != const.EHashMismatch:
                print "Failed, result: {}".format(result)
                print self.bp.response.json()
                ans = False
        return ans

    def upload(self,youtube_id):
        fpath = os.path.join(self.LDlDir,''.join([youtube_id,'.',self.ext]) )
        try:
            ans = self.bp.upload(localpath=fpath, remotepath=self.RDir, ondup=u'overwrite')
            resp = self._chkok(ans)
            print 'ans:'+str(ans)+';'
            if resp:
                self._addID(youtube_id,self.uploaded_video)
            return resp
                
        except Exception,e:
            print 'upload failed.'
            print self.bp.response.json()
            print e
            
#    def syncup(self):
#        assert self.processes > 1
#        try:
#            uplist = os.listdir(self.LDlDir) ##a,b = os.path.splitext()
#            ans = self.bp.syncup(self.LDlDir,self.RDir)
#            resp = self.chkok(ans)
#            if resp:                
#                self._addID(youtube_id,self.uploaded_video)
##        
            
    def process(self,youtube_id):
        if len(self.dlqueue) < self.que_max: #如果队列够少，就继续下载;如果队列足够self.que_max，就开始上传
            # download
            print '===== downloading... '
            if self.download(youtube_id):
                self.dlqueue.append(youtube_id)
        else:
            # upload and delete
            print '===== uploading... '
            for item in self.dlqueue: #.copy
                fpath = os.path.join(self.LDlDir,''.join([item,'.',self.ext]) )
                assert os.path.exists(fpath)
                ans = self.upload(item)
                if ans == True:
                    os.remove(fpath)
                    self.dlqueue.remove(item)
                    print str(item),' uploaded. deleted'
                else:
                    continue

    
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
#    workjob(youtubeid,path)
    #download(badid)
    w = TheParty(path)
    w.process(youtubeid)
    w.upload(youtubeid)
    w.process(badid)
