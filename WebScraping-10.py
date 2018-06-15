#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:27:11 2018

@author: mars
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time


#selenium函式
#find_element_by_id
#find_element(s)_by_name
#find_element(s)_by_xpath
#find_element(s)_by_link_text
#find_element(s)_by_partial_link_text
#find_element(s)_by_tag_name
#find_element(s)_by_class_name
#find_element(s)_by_css_selector(#id, .class, name, tag[attr=''])

#抓取範例文字
chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver'
driver = webdriver.Chrome(chromePath)
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
time.sleep(3)
print(driver.find_element_by_id('content').text)

driver.close() #close():關閉瀏覽器, quit():並釋放連線

#利用BeautifulSoup解析頁面
chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver'
driver = webdriver.Chrome(chromePath)
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
time.sleep(3)

pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource)
print(bsObj.find(id='content').text)

driver.close()

#