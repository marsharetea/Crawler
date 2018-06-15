#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:55:20 2018

@author: mars
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re
import json


#搜集 wikipedia 編輯紀錄裡的IP位址並結合 freegeoip API 顯示IP所在國家
random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org'+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find('div', id='bodyContent').findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

def getHistoryIPs(pageUrl):
    #編輯紀錄頁的網址格式：http://en.wikipedia.org/w/indix.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace('/wiki/', '')
    historyUrl = 'http://en.wikipedia.org/w/index.php?title='+pageUrl+'&action=history'
    print('history url is:', historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html)
    ipAddresses = bsObj.findAll('a', {'class':'mw-anonuserlink'})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.text)
    return addressList

links = getLinks('/wiki/Python_(programming_language)')

def getCountry(ipAddress):
    try:
        response = urlopen('http://freegeoip.net/json/'+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get('country_code')

while len(links) >0:
    for link in links:
        print('--------------------------------------------------------------------------')
        historyIPs = getHistoryIPs(link.attrs['href'])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP, 'is from', country)
    
    newLink = links[random.randint(1, len(links)-1)].attrs['href']
    links = getLinks(newLink)