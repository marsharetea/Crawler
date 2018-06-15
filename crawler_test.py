#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 01:55:57 2018

@author: mars
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

'''
quote_page = 'http://www.bloomberg.com/quote/SPX:IND'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

name_box = soup.find('h1', attrs={'class': 'name'})
name = name_box.text.strip() #去除前後空格
price_box = soup.find('div', attrs={'class':'price'})
price = price_box.text
ticker_box = soup.find('div', attrs={'class':'ticker'})
ticker = ticker_box.text

print(name, price, ticker)
'''

#FB test

quote_page = 'https://www.facebook.com/profile.php?id=100000436114872'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

name_box = soup.find('h1', attrs={'class': '_2nlv'})
name = name_box.text.strip() #去除前後空格

#print(name)

a = soup.find_all('a')
for a in a:
    print(a.text)


#PTT test
'''
import time
import requests

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')

    articles = []  #儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string == date:  #發文日期正確
            #取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  #轉換字串為數字
                except ValueError:  #若轉換失敗，不做任何事，push_count 保持為 0
                    pass

            #取得文章連結及標題			
            if d.find('a'):  #有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count
                })
    return articles

page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')
if page:
    date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
    current_articles = get_articles(page, date)
    for post in current_articles:
        print(post)
'''

