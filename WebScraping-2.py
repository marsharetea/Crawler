#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 23:16:23 2018

@author: mars
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html.read())

nameList = bsObj.findAll('span', {'class':'green'})
for name in nameList:
    print(name.get_text())

#findAll(tag, attributes, recursive, text, limit, keywords)
#find(tag, attributes, recursive, text, keywords)
#tag: findAll({'h1', 'h2', 'h3'})
#attributes: findAll('span', {'class': {'green', 'red'}})
#recursive: 欲深入到文件第幾層，預設值True
#text: 某段文字被包圍幾次
#limit: find = findAll(limit = 1)
#keyword: findAll(id='text')

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bsObj = BeautifulSoup(html.read())

#處理子代或子孫: .children or .descendants
for child in bsObj.find('table', {'id':'giftList'}).children:
    print(child)

#處理平輩: .next_siblings or .previous_siblings
for sibling in bsObj.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sibling)

#處理親代: .parent or .parents
print(bsObj.find('img', {'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.text)

#正規表達式
images = bsObj.findAll('img', {'src':re.compile('\.\.\/img\/gifts\/img.*\.jpg')})
for image in images:
    print(image['src'])

#lambda表達式
print(bsObj.find(lambda tag: len(tag.attrs) == 2))
