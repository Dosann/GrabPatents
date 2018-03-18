# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 14:36:43 2017

@author: Gavin
"""

import time
from sys import path
path.append(r'../')
import Crawl
from numpy import ceil

class SpiderPatents:
    
    def __init__(self,numberpercate,windowpara):
        self.numberpercate=numberpercate
        self.turnpage=ceil(numberpercate/50)
        self.windowpara=windowpara
    
    # begin crawling
    def BeginCrawling(self):
        self.c=Crawl.CrawlPatentProfile(self.windowpara)
        self.c.Login()
        self.c.JumpToCate()
        
    def CrawlMainProcess(self,startcate,startsubcate,startpage):
        result=self.c.CrawlPatents(startcate,startsubcate,startpage,self.numberpercate,self.turnpage)
        return result
    
    def CrawlUrl(self,rangeinfo):
        result=self.c.CrawlUrl(rangeinfo,self.numberpercate,self.turnpage)
        return result


startcate=int(input('startcate:'))
startsubcate=int(input('startsubcate:'))
endcate=int(input('endcate:'))
endsubcate=int(input('endsubcate:'))
startpage=int(input('startpage:'))
windowpara=['']*4
windowpara[0]=int(input('windowsizex:'))
windowpara[1]=int(input('windowsizey:'))
windowpara[2]=int(input('windowposx:'))
windowpara[3]=int(input('windowposy:'))
num_patents_persubcate = int(input('num_patents_persubcate:'))
'''
print sys.argv,len(sys.argv)
startcate=int(sys.argv[1])
startsubcate=int(sys.argv[2])
startpage=int(sys.argv[3])
endcate=int(sys.argv[4])
endsubcate=int(sys.argv[5])
'''

print("input finished")
windowpara=list(map(lambda x:int(x),windowpara))
s=SpiderPatents(1000,windowpara)
s.BeginCrawling()

rangeinfo=(startcate,startsubcate,startpage,endcate,endsubcate)
while rangeinfo!=True:
    rangeinfo=s.CrawlUrl(rangeinfo)
    if rangeinfo!=True:
        del(s)
        s=SpiderPatents(num_patents_persubcate,windowpara)
        s.BeginCrawling()