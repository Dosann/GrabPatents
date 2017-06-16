# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 12:18:17 2017

@author: Gavin
"""

import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
from string import strip
from MySQLdb import Connection

class SeleniumSupport:
    
    @staticmethod
    def PushButtonByXpath(driver,xpath):
        locator=(By.XPATH,xpath)
        WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located(locator))
        driver.find_element_by_xpath(xpath).click()
    
    @staticmethod
    def CountSubcate(driver):
        xpath="""//*[@id="ipc_result"]"""
        locator=(By.XPATH,xpath)
        WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located(locator))
        eles=driver.find_elements_by_class_name("ipc_c")
        count=len(eles)-1
        print "subcategory count:",count
        return count
    
    @staticmethod
    def CountPatent(driver):
        xpath="""//*[@id="pagetop"]/div[1]"""
        locator=(By.XPATH,xpath)
        WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located(locator))
        e=driver.find_element_by_xpath(xpath)
        count=int(Filter.FilterNumber(Filter.FilterNumber(e.text.split(' ')[-1])))
        return count
    
    @staticmethod
    def DownloadPatentInfo(driver,xpath):
        SeleniumSupport.WaitUntilClickable(driver,xpath)
        SeleniumSupport.PushButtonByXpath(driver,xpath)
        SeleniumSupport.PushButtonByXpath(driver,"""/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/input[1]""")
        SeleniumSupport.PushButtonByXpath(driver,"""/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/input[3]""")

    @staticmethod
    def WaitUntilPresence(driver,xpath):
        locator=(By.XPATH,xpath)
        WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located(locator))
    
    @staticmethod
    def WaitUntilPresenceByText(driver,xpath,link_text):
        #result=driver.find_element_by_xpath(xpath)
        locator=(By.LINK_TEXT,link_text)
        WebDriverWait(driver,20,1.5).until(EC.presence_of_element_located(locator))
    
    @staticmethod
    def WaitUntilClickable(driver,xpath):
        locator=(By.XPATH,xpath)
        WebDriverWait(driver,20,1.5).until(EC.element_to_be_clickable(locator))
        time.sleep(2)
        
    @staticmethod
    def WaitUntilTurnpageFinished(driver,reference):
        while driver.find_element_by_xpath("""//*[@id="divlist"]/ul/li[1]/div[1]/a""").text==reference:
            time.sleep(0.5)

    @staticmethod
    def GetTextByXpath(driver,xpath):
        SeleniumSupport.WaitUntilPresence(driver,xpath)
        txt=driver.find_element_by_xpath(xpath).text
        return strip(txt)
    
    @staticmethod
    def JumpPage(driver,page):
        #SeleniumSupport.WaitUntilPresence("""//*[@id="pagetop"]/table/tbody/tr/td[7]/input""")
        pagetextbox=driver.find_element_by_xpath("""//*[@id="pagetop"]/table/tbody/tr/td[7]/input""")
        pagetextbox.clear()
        pagetextbox.send_keys(str(page))
        time.sleep(0.5)
        pagetextbox.send_keys(Keys.ENTER)

class LoadData:
    
    @staticmethod
    def LoadDataByIdRange(conn,tablename,columns,rangeinfo):
        cur=conn.cursor()
        cmd="""select %s from %s where id>=%s and id<=%s"""%(columns,tablename,rangeinfo[0],rangeinfo[1])
        columncount=len(columns.split(','))
        cur.execute(cmd)
        data=cur.fetchall()
        data=map(lambda x:x[0:columncount],data)
        cur.close()
        return data


class SaveData:
    
    @staticmethod
    def GenerateColumns(columns):
        columnsize=len(columns)
        columns=tuple(columns)
        s="("+"%s,"*(columnsize-1)+"%s)"
        s=s%(columns)
        return s
    
    @staticmethod
    def SaveBinaryData(conn,data,tablename):
        cur=conn.cursor()
        cmd="""insert into """+tablename+""" values(null,%s,%s)"""
        cur.executemany(cmd,data)
        conn.commit()
        cur.close()
    
    @staticmethod
    def SaveData(conn,data,tablename,columns):
        cur=conn.cursor()
        cmd="""insert into """+tablename+SaveData.GenerateColumns(columns)+""" values"""+SaveData.GenerateColumns(('%s',)*len(columns))
        cur.executemany(cmd,data)
        conn.commit()
        cur.close()

class DatabaseSupport:
    
    @staticmethod
    def GenerateConn():
        conn=Connection(
            host="localhost",
            port=3306,
            user='root',
            passwd='123456',
            db='grabpatents',
            charset='utf8')
        return conn
    
    @staticmethod
    def DatabaseConstruction(conn):
        cur=conn.cursor()
        cur.execute("""show tables""")
        tables=map(lambda ta:ta[0],cur.fetchall())
        
        if 'patentdetails' not in tables:
            DatabaseSupport.CreatePatentdetails(cur)
    
    @staticmethod
    def CreatePatentdetails(cur):
        cmd="""create table patentdetails(id int auto_increment primary key,originid int,
                                          mingchen varchar(200),shenqinghao varchar(14),shenqingri varchar(10),guojiashengshi varchar(20),
                                          gongkaihao varchar(10),gongkairi varchar(10),
                                          zhufenleihao varchar(22),sqgongkaihao varchar(10),sqgongkairi varchar(10),fenleihao varchar(2000),
                                          shenqingren varchar(100),famingren varchar(200),dailiren varchar(30),dailijigou varchar(50),
                                          shenqingrendizhi varchar(100),youxianquan varchar(200),zhaiyao varchar(2000),zhuquanliyaoqiu text,
                                          falvzhuangtai varchar(5),url varchar(200))"""
        cur.execute(cmd)
        
        
class Filter:
    
    @staticmethod
    def FilterNumber(s):
        result=re.findall('\d+',s)
        if len(result)==0:
            print "error: can't find numbers"
        else:
            return result[0]
    
    @staticmethod
    def FilterPatentApplicantId(s):
        return s.split(u'：')[-1]
    
    @staticmethod
    def FilterCateindex(s):
        cateindex=s.split(' ')[0]
        if cateindex==s or len(cateindex)>9:
            cateindex=cateindex[0:4]
        return cateindex
    
    @staticmethod
    def FilterFalvzhuangtai(s):
        res=re.findall("\S+",s)
        if len(res)==0:
            return ""
        result=res[1][-2:]
        
        return result