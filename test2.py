# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 10:12:32 2017

@author: Gavin
"""

from sys import path
import Crawl
import Queue
import Tools
import threading
from numpy import floor
from os import system

def CrawlPatentDetails(threadname,que,windowpara):
    download_count=0
    restart_count=0
    
    print threadname,"successfully started"
    c=Crawl.CrawlPatentProfile(windowpara)
    status,download_count_iter=c.CrawlPatentsByUrl(threadname,que)
    download_count+=download_count_iter
    restart_count+=1
    
    print threadname,"finished. restart count:",restart_count
    print '\t',"download count:",download_count
    
que=Queue.Queue(maxsize=300000)
conn=Tools.DatabaseSupport.GenerateConn()
urls=Tools.LoadData.LoadDataByIdRange(conn,"patenturl","id,url",(850,900))
for url in urls:
    que.put(url)
CrawlPatentDetails("MainThread",que,(600,600,200,200))