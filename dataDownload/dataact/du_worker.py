#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import argparse
import time
import threading

from bypy import ByPy, const
import youtube_dl

from downlib.JsonLoader import readJsonSet
from downlib.readCSV import readCSVSet
from downlib.readTXT import readTXTSet
'''
python doanload3.py data/kinetics-400_test.csv download
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ

'''
class TheParty(object):
    def __init__(self,dataset,remote_path,localDlDir='tmp'):
        self.alldown = list(dataset)
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
        self.que_max = 50
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
#            resp = self._chkok(ans)
#            for item in uplist:
#                file,_ = os.path.splitext(item)
#                if not resp:
#                    ans = self.upload(item)
#                    assert self._chkok(ans)
#                os.remove(fpath)
#                self.dlqueue.remove(item)
#                print str(item),' uploaded. deleted'
#                self._addID(item,self.uploaded_video)
#                
#        except Exception,e:
#            print 'upload failed.'
#            print self.bp.response.json()
#            print e

    def worker_updel(self):
        while len(self.dlqueue) > 0:
            item = self.dlqueue.pop()
            print 'upload and delete ',item
            fpath = os.path.join(self.LDlDir,''.join([item,'.',self.ext]) )
            try:
                assert os.path.exists(fpath)
            except Exception,e:
                print e               
            ans = self.upload(item)
            if ans == True:
                os.remove(fpath)
                print str(item),' uploaded. deleted'
            else:
                self.dlqueue.append(item)
                continue
    
    def worker_download(self):
        while len(self.alldown) > 0:
            if len(self.dlqueue) < self.que_max: #如果队列够少，就继续下载;如果队列足够self.que_max，就开始上传
                # download
                item = self.alldown.pop()
                print '===== downloading... ',item
                if self.download(item):
                    self.dlqueue.append(item)
            
    def process(self):
        t1 = threading.Thread(target = self.worker_updel)
        t2 = threading.Thread(target = self.worker_download)#,args = (8,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
                    

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
    badfiles = ['bad_video.log','act100.txt','act200.txt','k400.txt','bdnet.txt']
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
    dataset = readSet(args.input_file,args.fmt)
    if args.no_bad == False:
        dataset = setOp(dataset)
        
    aworker = TheParty(dataset,args.output_dir)    
    aworker.process()

    

    
if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input_file',type=str, help=('input file name')) 
    p.add_argument('fmt',type=str,default='json',choices=['json','txt','csv'],help=('Input file format') ) 
    p.add_argument('output_dir',type=str, help=('Output directory where videos will be saved.') ) 
    p.add_argument('--no_bad', '--force', default=False, action="store_true")
    #p.add_argument('-n', '--num-jobs', type=int, default=2)
    #main(**vars(p.parse_args() ) )
    main( p.parse_args() )
    
