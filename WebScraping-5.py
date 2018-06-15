#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:33:37 2018

@author: mars
"""

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os
import csv
import smtplib
from email.mime.text import MIMEText
import pymysql


#下載單一檔案
html = urlopen('http://www.pythonscraping.com')
bsObj = BeautifulSoup(html)
imageLocation = bsObj.find('a', id = 'logo').find('img')['src']
urlretrieve(imageLocation, '/Users/mars/Desktop/logo.jpg')

#下載網站內全部檔案
downloadDirectory = '/Users/mars/Desktop/downloaded'
baseUrl = 'http://pythonscraping.com'

def getAbsoluteUrl(baseUrl, source):
    if source.startswith('http://www.'):
        url = 'http://'+source[11:]
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = 'http://'+source[4:]
    else:
        url = baseUrl+'/'+source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('www', '')
    path = path.replace(baseUrl, '')
    path = downloadDirectory+path
    directory = os.path.dirname(path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return path

html = urlopen(baseUrl)
bsObj = BeautifulSoup(html)
downloadList = bsObj.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteUrl(baseUrl, download['src'])
    if fileUrl is not None:
        print('ok:\t', fileUrl)
        urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))

#data to csv
csvFile = open('/Users/mars/Desktop/test.csv', 'w+', newline='')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number +2', 'number *2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()

#儲存比較表格至csv檔
html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bsObj = BeautifulSoup(html)

table = bsObj.findAll('table', {'class':'wikitable'})[0] #頁面裡的第一個表格
rows = table.findAll('tr')

csvFile = open('/Users/mars/Desktop/editors.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.text)
        writer.writerow(csvRow)
finally:
    csvFile.close()

#SMTP
msg = MIMEText("The body of the email is here")

msg['Subject'] = "An Email Alert"
msg['From'] = "jason31015@gmail.com"
msg['To'] = "jason31015@gmail.com"

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

#PyMySQL
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', charset='utf8', autocommit=True)

cur = conn.cursor()
cur.execute("USE social_network")
cur.execute("SELECT * FROM businessHR")

print(cur.fetchone())

cur.close()
conn.close()

