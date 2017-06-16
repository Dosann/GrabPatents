# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 12:14:06 2017

@author: Gavin
"""

from selenium import webdriver
import time
import MySQLdb
import Tools
from string import strip
import traceback


class CrawlPatentProfile:
    
    def __init__(self,windowpara):
        self.baseurl="""http://search.patentstar.com.cn/frmLogin.aspx"""
        self.cateurl="""http://search.patentstar.com.cn/My/frmIPCSearch.aspx"""
        
        self.conn=MySQLdb.Connection(
                    host="localhost",
                    port=3306,
                    user='root',
                    passwd='123456',
                    db='grabpatents',
                    charset='utf8')
        
        self.driver=webdriver.PhantomJS()
        '''
        chromeOptions=webdriver.ChromeOptions()
        prefs={"download.default_directory":"D:\Codes\PythonGrabPatents\PatentFiles"}
        chromeOptions.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        '''
        
        self.driver.set_window_size(windowpara[0],windowpara[1])
        self.driver.set_window_position(windowpara[2],windowpara[3])
        
        Tools.DatabaseSupport.DatabaseConstruction(self.conn)
        
        self.Login()
        self.JumpToCate()
        
        
    def Login(self):
        self.driver.get(self.baseurl)
        username=self.driver.find_element_by_name("TextBoxAccount")
        username.clear()
        username.send_keys("Kevin DU")
        password=self.driver.find_element_by_name("Password")
        password.clear()
        password.send_keys("a19960407")
        self.driver.find_element_by_id("ImageButtonLogin").click()
    
    def JumpToCate(self):
        self.driver.get(self.cateurl)
        
    def CrawlPatents(self,cateindex,subcateindex,pageindex,numberpercate,turnpage,patentnumber):
        self.patentnumber=patentnumber
        i=cateindex
        j=subcateindex
        currentpage=pageindex
        try:
            i=cateindex
            while i<9:
                print i
                catexpath="""//*[@id="listIPC"]/li["""+str(i)+"""]/a"""
                Tools.SeleniumSupport.PushButtonByXpath(self.driver,catexpath)
                time.sleep(2)
                subcateCount=Tools.SeleniumSupport.CountSubcate(self.driver)
                
                
                j=subcateindex
                
                if i==cateindex:
                    j=subcateindex
                
                while j<subcateCount+1:
                    print i,j
                    subcatexpath="""//*[@id="ipc_result"]/li["""+str(j+1)+"""]/div[3]/span[1]"""
                    if i!=cateindex or j!=subcateindex:
                        self.JumpToCate()
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,catexpath)
                    Tools.SeleniumSupport.WaitUntilClickable(self.driver,catexpath)
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,catexpath)
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,subcatexpath)
                    Tools.SeleniumSupport.WaitUntilClickable(self.driver,subcatexpath)
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,subcatexpath)
                    page50xpath="""//*[@id="pagetop"]/table/tbody/tr/td[1]/select/option[4]"""
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,page50xpath)
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="divlist"]/ul/li[50]/div[1]/a""")
                    patentcount=Tools.SeleniumSupport.CountPatent(self.driver)
                    
                    if patentcount<numberpercate:
                        number=numberpercate
                        patentpagelist=[]
                        while number>50:
                            patentpagelist.append(50)
                            number+=-50
                        patentpagelist.append(number)
                    else:
                        patentpagelist=[50]*(turnpage-1)
                        patentpagelist.append(int(numberpercate-(turnpage-1)*50))
                    pagecount=len(patentpagelist)
                    currentpage=1
                    
                    if i==cateindex and j==subcateindex and currentpage!=pageindex:
                        currentpage=pageindex
                        time.sleep(1)
                        Tools.SeleniumSupport.JumpPage(self.driver,currentpage)
                        
                    while True:
                        print i,j,currentpage,time.ctime()
                        time.sleep(2)
                        #for k in range(1,3):
                        for k in range(1,patentpagelist[currentpage]+1):
                            downloadxpath="""//*[@id="divlist"]/ul/li["""+str(k)+"""]/div[3]/div[2]/a[2]"""
                            Tools.SeleniumSupport.WaitUntilPresence(self.driver,downloadxpath)
                            Tools.SeleniumSupport.WaitUntilClickable(self.driver,downloadxpath)
                            Tools.SeleniumSupport.DownloadPatentInfo(self.driver,downloadxpath)
                        time.sleep(2)
                        currentpage+=1
                        if currentpage>=pagecount:
                            break;
                        Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                        Tools.SeleniumSupport.WaitUntilClickable(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                        Tools.SeleniumSupport.PushButtonByXpath(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                    j+=1
                i+=1
        except:
            print "error:",i,j,currentpage
            self.driver.close()
            return [i,j,currentpage]
        return True

    def CrawlUrl(self,rangeinfo,numberpercate,turnpage,patentnumber):
        self.patentnumber=patentnumber
        cateindex,subcateindex,pageindex,endcateindex,endsubcateindex=rangeinfo
        i=cateindex
        j=subcateindex
        currentpage=pageindex
        try:
            i=cateindex
            while i<9 and i<=endcateindex:
                print i
                if i!=cateindex or j!=subcateindex:
                    self.JumpToCate()
                catexpath="""//*[@id="listIPC"]/li["""+str(i)+"""]/a"""
                Tools.SeleniumSupport.PushButtonByXpath(self.driver,catexpath)
                time.sleep(2)
                subcateCount=Tools.SeleniumSupport.CountSubcate(self.driver)
                
                
                if i==cateindex:
                    j=subcateindex
                
                while j<subcateCount+1 and (i<endcateindex or j<=endsubcateindex):
                    print i,j
                    subcatexpath="""//*[@id="ipc_result"]/li["""+str(j+1)+"""]/div[3]/span[1]"""
                    if i!=cateindex or j!=subcateindex:
                        self.JumpToCate()
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,catexpath)
                    Tools.SeleniumSupport.WaitUntilClickable(self.driver,catexpath)
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,catexpath)
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,subcatexpath)
                    Tools.SeleniumSupport.WaitUntilClickable(self.driver,subcatexpath)
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,subcatexpath)
                    page50xpath="""//*[@id="pagetop"]/table/tbody/tr/td[1]/select/option[4]"""
                    Tools.SeleniumSupport.PushButtonByXpath(self.driver,page50xpath)
                    Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="divlist"]/ul/li[50]/div[1]/a""")
                    patentcount=Tools.SeleniumSupport.CountPatent(self.driver)
                    
                    if patentcount<numberpercate:
                        number=patentcount
                        patentpagelist=[]
                        while number>50:
                            patentpagelist.append(50)
                            number+=-50
                        patentpagelist.append(number)
                    else:
                        patentpagelist=[50]*(turnpage-1)
                        patentpagelist.append(int(numberpercate-(turnpage-1)*50))
                    pagecount=len(patentpagelist)
                    currentpage=1
                    
                    if i==cateindex and j==subcateindex and currentpage!=pageindex:
                        currentpage=pageindex
                        time.sleep(1)
                        Tools.SeleniumSupport.JumpPage(self.driver,currentpage)
                    
                    reference=''
                    while True:
                        print i,j,currentpage,time.ctime()
                        time.sleep(1)
                        Tools.SeleniumSupport.WaitUntilTurnpageFinished(self.driver,reference)
                        
                        #for k in range(1,3):
                        datapairs=['']*patentpagelist[currentpage-1]
                        for k in range(patentpagelist[currentpage-1]):
                            #print k
                            Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="divlist"]/ul/li[%s]/div[1]/a"""%(k+1,))
                            Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="divlist"]/ul/li[%s]/div[3]/div[1]/div[1]/div[1]"""%(k+1,))
                            Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="divlist"]/ul/li[%s]/div[3]/div[1]/div[2]/a"""%(k+1,))
                            
                            applicantid=Tools.Filter.FilterPatentApplicantId(self.driver.find_element_by_xpath("""//*[@id="divlist"]/ul/li[%s]/div[3]/div[1]/div[1]/div[1]"""%(k+1,)).text)
                            url=self.driver.find_element_by_xpath("""//*[@id="divlist"]/ul/li[%s]/div[1]/a"""%(k+1,)).get_attribute('href')
                            cateindex=Tools.Filter.FilterCateindex(self.driver.find_element_by_xpath("""//*[@id="divlist"]/ul/li[%s]/div[3]/div[1]/div[2]/a"""%(k+1,)).text)
                            datapairs[k]=(applicantid,cateindex,url)
                        reference=self.driver.find_element_by_xpath("""//*[@id="divlist"]/ul/li[1]/div[1]/a""").text
                        Tools.SaveData.SaveData(self.conn,datapairs,'patenturl',['applicantid','cateindex','url'])
                        print 'successfully saved. inserted items count:',len(datapairs),'pos:',i,j,currentpage
                        currentpage+=1
                        if currentpage>pagecount:
                            break
                        Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                        Tools.SeleniumSupport.WaitUntilClickable(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                        Tools.SeleniumSupport.PushButtonByXpath(self.driver,"""//*[@id="pagetop"]/table/tbody/tr/td[10]/a/span/span/span""")
                    j+=1
                i+=1
                j=1
        
        except Exception,e:
            print "error:",i,j,currentpage
            print e
            self.driver.close()
            return [i,j,currentpage,endcateindex,endsubcateindex]
        
        return True
        
    def CrawlPatentsByUrl(self,threadname,que):
        self.que=que
        download_count=0
        while not que.empty():
            try:
                current,url=que.get()
                print current,time.ctime()
                self.driver.get(url)
                mingchen=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/b/span""")
                shenqinghao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tdApno"]""")
                shenqingri=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[1]/td[4]""")
                guojiashengshi=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[1]/td[6]""")
                gongkaihao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="trFmXx"]/td[2]""")
                gongkairi=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="trFmXx"]/td[4]""")
                zhufenleihao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="trFmXx"]/td[6]""")
                sqgongkaihao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[3]/td[2]""")
                sqgongkairi=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[3]/td[4]""")
                fenleihao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[3]/td[6]""")
                shenqingren=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[4]/td[2]""")
                famingren=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[5]/td[2]""")
                dailiren=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[6]/td[2]""")
                dailijigou=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[7]/td[2]""")
                shenqingrendizhi=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[8]/td[2]""")
                youxianquan=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[9]/td[2]""")
                zhaiyao=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="tabMianXml"]/table[1]/tbody/tr[10]/td/span""")
                zhuquanliyaoqiu=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="LabelClaim"]/span""")
                '''
                Tools.SeleniumSupport.WaitUntilClickable(self.driver,"""//*[@id="ulPatTabs"]/li[5]""")
                Tools.SeleniumSupport.PushButtonByXpath(self.driver,"""//*[@id="ulPatTabs"]/li[5]""")
                for i in range(5):
                    falv=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="ctl00_ContentPlaceHolder1_GridViewLegal"]/tbody/tr[2]/td/div/div[2]""")
                    if len(falv)!=0:
                        break
                    else:
                        time.sleep(0.5)
                
                time.sleep(1)
                Tools.SeleniumSupport.WaitUntilPresence(self.driver,"""//*[@id="ctl00_ContentPlaceHolder1_GridViewLegal"]/tbody/tr[2]/td/div/div[2]/b[2]""")
                falv=Tools.SeleniumSupport.GetTextByXpath(self.driver,"""//*[@id="ctl00_ContentPlaceHolder1_GridViewLegal"]/tbody/tr[2]/td/div/div[2]/b[2]""")
                falvzhuangtai=falv
                #falvzhuangtai=Tools.Filter.FilterFalvzhuangtai(falv)
                print falv
                '''
                falvzhuangtai=""
                
                
                details=[(current,mingchen,shenqinghao,shenqingri,guojiashengshi,gongkaihao,gongkairi,zhufenleihao,sqgongkaihao,
                         sqgongkairi,fenleihao,shenqingren,famingren,dailiren,dailijigou,shenqingrendizhi,youxianquan,
                         zhaiyao,zhuquanliyaoqiu,falvzhuangtai,url)]
                columns=['originid','mingchen','shenqinghao','shenqingri','guojiashengshi','gongkaihao','gongkairi','zhufenleihao','sqgongkaihao','sqgongkairi','fenleihao',
                         'shenqingren','famingren','dailiren','dailijigou','shenqingrendizhi','youxianquan','zhaiyao','zhuquanliyaoqiu','falvzhuangtai','url']
                Tools.SaveData.SaveData(self.conn,details,"patentdetails",columns)
                print threadname,"successfully saved details of patent:",current,time.ctime()
                download_count+=1
            except Exception,e:
                print threadname,"Error when crawling, current patent:",current
                print e
                traceback.print_exc()
                self.que.put((current,url))
                print "Failed mission has been put back into que:",current
                self.driver.quit()
                self.conn.close()
                return False,download_count
        self.driver.quit()
        self.conn.close()
        return True,download_count
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            