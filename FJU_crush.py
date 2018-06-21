#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:42:41 2018

@author: mars
"""

from selenium import webdriver
import time
#import getpass
#import re
#import csv
import re
import pymysql
import datetime


#FJU CRUSH scrape
def main():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2} #關閉chrome通知提醒
    chrome_options.add_experimental_option("prefs",prefs)

    chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver' #chromedriver path
    driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)
    driver.get('https://www.facebook.com')
    
    _login(driver) #登入FB
    
    fju_crush = "https://www.facebook.com/FJUCrush/"
    _scrape_article(driver, fju_crush) #搜尋告白文章
        
    _upload_db(crush_article) #匯入至 angel_pair > confession
    
    driver.close()
    
def _login(driver):
    #account = input('input your account:')
    #passwd = getpass.getpass("input your password:")
    account = "0926983921"
    passwd = 'puo053434'
    
    driver.find_element_by_id("email").clear() #清除欄位
    driver.find_element_by_id("email").send_keys(account) #輸入帳號
    print('Account entered...')
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys(passwd) #輸入密碼
    print('Password entered...')
    driver.find_element_by_id("loginbutton").click() #按下登入

def _scrape_article(driver, href):
    driver.get(href)
    
    time.sleep(1)
    #_scroll_to_bottom(driver, 1)
    
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='_1xnd']/div[@class='_1xnd']/div/div[@class='_4z-w']/a").click() #顯示全部貼文
    
    time.sleep(3)
    article_context = driver.find_elements_by_css_selector("._5pbx")

    global crush_article

    latest_head = _check_duplicate()
    print(latest_head)
    
    for context in article_context:
        crush = re.split('#|更多', context.text)
        if not re.match(latest_head, crush[0]):
            crush_article.append(crush[0].strip("\n"))
            print(crush[0], "\n---------------------------------------------------------")
        else:
            break

def _scroll_to_bottom(driver, scroll_count):
    scroll_pause_time = 0.8

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    current_count = 0
    #while True:
    while current_count < scroll_count:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(scroll_pause_time+0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return
        
        last_height = new_height
        current_count += 1

def _check_duplicate():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', charset='utf8', autocommit=True)
    
    cur = conn.cursor()
    cur.execute("USE angel_pair")
    cur.execute("SELECT `head` FROM `confession` WHERE `head` LIKE '%告白輔大%' ORDER BY `date` DESC, `time` DESC,`articleid` ASC LIMIT 1")
    
    latest_head = cur.fetchone()
    
    return latest_head[0][6:-3]

def _upload_db(article_list):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', charset='utf8', autocommit=True)
    
    cur = conn.cursor()
    cur.execute("USE angel_pair")
    
    date = datetime.datetime.now().strftime("%Y/%m/%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    
    cur.executemany("INSERT INTO confession(userid, date, time, head, article) VALUES (1, %s, %s, %s, %s)", [(date, time, "＃告白輔大 "+article[:15]+"...", article[:]) for article in article_list])
    
    cur.close()
    conn.close()
    print("Upload to SQL successful...")


crush_article = list()
main()

