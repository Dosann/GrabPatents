# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 10:14:27 2017

@author: Gavin
"""

import time
from sys import path
path.append(r'../')
import Crawl
import queue
import Tools
import threading
from numpy import floor
from os import system

def CrawlPatentDetails(threadname,que,windowpara):
    download_count=0
    restart_count=0
    while True:
        print(threadname,"successfully started")
        c=Crawl.CrawlPatentProfile(windowpara)
        status,download_count_iter=c.CrawlPatentsByUrl(threadname,que)
        download_count+=download_count_iter
        if status==True:
            break
        restart_count+=1
    print(threadname,"finished. restart count:",restart_count)
    print('\t',"download count:",download_count)


if __name__=='__main__':
    que=queue.Queue(maxsize=300000)
    conn=Tools.DatabaseSupport.GenerateConn()
    urls=Tools.LoadData.LoadDataByIdRange(conn,"patenturl","id,url",(1,200000))
    for url in urls:
        que.put(url)
    threads=[]
    threadnumber=12
    for i in range(threadnumber):
        y=floor(i/6)*300
        x=(i%6)*200
        windowpara=(180,300,x,y)
        t=threading.Thread(target=CrawlPatentDetails,args=("Thread-%s"%(i+1),que,windowpara,))
        t.setDaemon(True)
        threads.append(t)
        t.start()
    i=0
    for t in threads:
        t.join()
        print("Thread-%s"%(i+1),"has been joined")
        i+=1
    #time.sleep(80)
    print("successfully finished")
    system("pause")