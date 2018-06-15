#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 02:25:30 2018

@author: mars
"""

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import random
import datetime


html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bsObj = BeautifulSoup(html.read())

#判斷tag 裡是否有 'href'
for link in bsObj.findAll('a'):
    if 'href' in link.attrs:
        print(link.attrs['href'])

#URL都以 /wiki/ 開頭且不包含 ':'
for link in bsObj.find('div', id='bodyContent').findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])

#函式形式寫成 getLinks()
random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org'+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find('div', id='bodyContent').findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)    

#爬行新的連結
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org'+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs and link.attrs['href'] not in pages:
            newPage = link.attrs['href']
            print(newPage)
            pages.add(newPage)
            getLinks(newPage)

getLinks('')

#爬行新的連結並顯示標題
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org'+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id='mw-content-text').findAll('p')[0].text)
        print(bsObj.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! No worries though!')
    
    for link in bsObj.findAll('a', href=re.compile('^(/wiki).*$')):
        if 'href' in link.attrs and link['href'] not in pages:
            newPage = link['href']
            print('--------------------------------------------\n'+newPage)
            pages.add(newPage)
            getLinks(newPage)

getLinks('')

#爬行不同的網站
pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    for link in bsObj.findAll('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] == None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    for link in bsObj.findAll('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace('http://', '').split('/')
    return addressParts

def getRandomExternalLink(startingPage):
    try:
        html = urlopen(startingPage)
        bsObj = BeautifulSoup(html)
    except HTTPError:
        print('Link is not open!')
        domain = urlparse(startingPage).scheme+'://'+urlparse(startingPage).netloc
        followExternalOnly(domain)

    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one!')
        domain = urlparse(startingPage).scheme+'://'+urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        if len(internalLinks) == 0:
            return None
        else:
            return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    if externalLink is not None:
        print('Random external link is:', externalLink)
        followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')

#搜集網站上找到的所有外部連結
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print('About to get link', link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

getAllExternalLinks('http://oreilly.com')

