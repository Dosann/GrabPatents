# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 14:54:17 2017

@author: Gavin
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import selenium.webdriver.common.desired_capabilities as DC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
import Tools
import re

'''
chromeOptions=webdriver.ChromeOptions()
prefs={"download.default_directory":"D:\Codes\PythonGrabPatents\PatentFiles"}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
'''
driver=webdriver.PhantomJS()

driver.get("""http://search.patentstar.com.cn/frmLogin.aspx""")
username=driver.find_element_by_name("TextBoxAccount")
username.clear()
username.send_keys("Kevin DU")
password=driver.find_element_by_name("Password")
password.clear()
password.send_keys("a19960407")
driver.find_element_by_id("ImageButtonLogin").click()
Tools.SeleniumSupport.WaitUntilClickable(driver,"""//*[@id="Smartnavbom"]/ul/li[1]/a/img""")
driver.find_element_by_xpath("""//*[@id="Smartnavbom"]/ul/li[1]/a/img""").click()
Tools.SeleniumSupport.WaitUntilClickable(driver,"""//*[@id="listIPC"]/li[1]/a""")
driver.find_element_by_xpath("""//*[@id="listIPC"]/li[1]/a""").click()
time.sleep(2)

driver.get(u"""http://search.patentstar.com.cn/my/frmPatDetails.aspx?Id=9CFA4DBA8HAAEHIA9CIC8AHA8EDA8CAAAIAABHEA9GED9AIG&xy=16318727&qy=%20(A01%2FIC)""")

txt=driver.find_element_by_xpath("""//*[@id="ctl00_ContentPlaceHolder1_GridViewLegal"]/tbody/tr[2]/td/div/div[2]""").text
print txt

#result=driver.find_element_by_xpath("""//*[@id="divlist"]/ul""")