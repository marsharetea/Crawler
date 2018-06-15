#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 19:29:55 2018

@author: mars
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


html = urlopen('http://www.pythonscraping.com/pages/page1.html')
bsObj = BeautifulSoup(html.read()) #html convert to BeautifulSoup物件
print(bsObj.h1) #bsObj物件裡 'h1' tag


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e: #連線錯誤 404 or 500 Error
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e: #not found server導致 bsObj為 None物件
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)