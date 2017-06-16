# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:56:15 2017

@author: duxin
"""

import csv
import os

rootdir="""D:\Codes\PythonGrabPatents\PatentFiles"""
filelist=[]
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filelist.append(filename)


patentsinfo=[]

csvfile=file('PatentFiles\\'+filelist[0],'r')
reader=csv.reader(csvfile)
title=[]
current=0
for line in reader:
    if current==0:
        for item in line:
            title.append(item)
    current+=1
#title[-1]=title[-1][:-1]
patentsinfo.append(title)

for patent in filelist:
    csvfile=file('PatentFiles\\'+patent,'r')
    reader=csv.reader(csvfile)
    patentline=[]
    current=0
    for line in reader:
        if current>0:
            for item in line:
                patentline.append(item)
        current+=1
    csvfile.close()
    #patentline[-1]=patentline[-1][:-1]
    patentsinfo.append(patentline)
    
patentsinfo_derepeat=[]
patentsinfo_derepeat.append(patentsinfo[0])
patentid=set()
for i in range(1,len(patentsinfo)):
    try:
        if patentsinfo[i][0] not in patentid:
            patentid.add(patentsinfo[i][0])
            patentsinfo_derepeat.append(patentsinfo[i])
    except:
        continue

f=open('patentinfo_archive.txt','w')
for line in patentsinfo_derepeat:
    for item in line:
        f.write(item+'\t')
    f.write('\n')
f.close()

'''
csvfile=file('patentinfo_archive.csv','w')
writer=csv.writer(csvfile)
writer.writerows(patentsinfo)
csvfile.close()
os.system("pause")
'''
