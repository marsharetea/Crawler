#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 14:43:38 2018

@author: mars
"""

from selenium import webdriver
import time
#import getpass
import re
import csv
import pymysql


#FB profile test
def main(): 
    start_time = time.time()
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2} #關閉chrome通知提醒
    chrome_options.add_experimental_option("prefs",prefs)

    chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver' #chromedriver path
    driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)
    driver.get('https://www.facebook.com') #Facebook首頁
    
    _login(driver) #登入FB

    profile_href = driver.find_element_by_xpath('//div[@class="_1k67 _cy7"]/a').get_attribute('href') #個人首頁網址
    _search_friend(driver, profile_href) #巢狀搜尋好友

    friends_info_indexed = _indexed_info(friends_info_set) #編列索引
    friends_link_standard = _standard_link(friends_link_list) #正規劃(去除Null值& 別稱& 重複值)
    
    _convert_to_csv(friends_info_indexed, friends_link_standard) #輸出成csv檔
    _upload_db(friends_info_indexed, friends_link_standard) #匯入至MySQL

    driver.close() #關閉瀏覽器
    
    _spend_time(start_time) #計算花費時間

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

def _search_friend(driver, href, count=0, depth=2):
    driver.get(href)
    
    try:
        #time.sleep(1)
        driver.find_element_by_xpath('//a[@data-tab-key="friends"]').click() #朋友
    except:
        try:
            time.sleep(2)
            driver.find_element_by_xpath('//a[@data-tab-key="friends"]').click() #朋友
        except:
            print('No "friend" button!\n------------------------')
            return
    try:
        time.sleep(1)
        #driver.find_element_by_xpath('//a[@class="_3c_"]').click() #共同朋友
        driver.find_element_by_name('共同朋友').click()
    except:
        try:
            time.sleep(2)
            driver.find_element_by_name('共同朋友').click()
        except:
            if count != 0:
                print('No "co-friends" button!\n------------------------')
                return
    
    _scroll_to_bottom(driver) #滑動頁面至底部
    
    friends_name_now = driver.find_element_by_xpath('//span[@data-testid="profile_name_in_profile_page"]/a').text
    friends_elem = driver.find_elements_by_xpath('//div[@class="uiProfileBlockContent"]/div/div/div/a')
    
    print(friends_name_now, '\n------------------------')
    
    global friends_info_set
    friends_info_set = friends_info_set | set([friends_name_now.split('\n')[0]]) | set([f.text for f in friends_elem]) #儲存個人資料
    global friends_link_list
    friends_link_list += [[friends_name_now, f.text] for f in friends_elem] #儲存關係連結
    
    if count+1 >= depth:
        return
    else:
        recursive_count = 0
        #friends_href = driver.find_elements_by_xpath('//div[@class="uiProfileBlockContent"]/div/div/a') #好友頁面網址
        for href in [f.get_attribute('href') for f in friends_elem]:
            if recursive_count >= 5:
                break
            if not re.match('.*#$', href): #檢查頁面是否存在
                recursive_count += 1
                print(recursive_count, end=', ')
                _search_friend(driver, href, count+1)
    
    print('Recursive count:', recursive_count)

def _scroll_to_bottom(driver):
    scroll_pause_time = 0.8

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_count = 0
    while True:
    #while scroll_count < 2:
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
        scroll_count += 1

def _indexed_info(theSet):    
    theList = list(theSet)
    try:
        theList.remove('')
    except:
        print('No "Null" value!')

    theDict_indexed = {}
    for i in range(len(theList)):
        theDict_indexed[theList[i]] = i+1
    print('Indexed information...')
    return theDict_indexed

def _standard_link(theList):
    theList_standard = []
    for link in theList:
        if link[1] is not '':
            link[0] = link[0].split('\n')[0]
            theList_standard.append(link)
    _eliminate_duplication_link(theList_standard)
    print('Standard friends-link...')
    return theList_standard

def _eliminate_duplication_link(theList):
    for link in theList:
        f = link[0]
        t = link[1]
        for link2 in theList:
            f2 = link2[0]
            t2 = link2[1]
            if f == t2 and t == f2:
                theList.remove(link2)
                break
    print('Eliminate duplication-link...')

def _convert_to_csv(theDict, theList):
    csvFile = open('/Users/mars/Desktop/friends_info.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(('id', 'name'))
        for _name, _id in theDict.items():
            writer.writerow((_id, _name))
    finally:
        csvFile.close()
    
    csvFile = open('/Users/mars/Desktop/friends_link.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(('from', 'id1', 'to', 'id2'))
        for link in theList:
            writer.writerow([theDict[link[0]], link[0], theDict[link[1]], link[1]])
    finally:
        csvFile.close()
    print('Loadfile CSV successful...')

def _upload_db(theDict, theList):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='1234', charset='utf8', autocommit=True)
    
    cur = conn.cursor()
    cur.execute("USE social_network")
    
    try:
        cur.execute("DROP TABLE facebook_info")
        cur.execute("DROP TABLE facebook_link")
    except:
        print("The table is not find...")
    
    cur.execute("CREATE TABLE facebook_info(id int(10), name varchar(100))")
    cur.execute("CREATE TABLE facebook_link(`from` int(10), id1 varchar(100), `to` int(10), id2 varchar(100))")
    
    cur.executemany("INSERT INTO facebook_info(id, name) VALUES (%s, %s)", [(_id, _name) for _name, _id in theDict.items()])
    cur.executemany("INSERT INTO facebook_link(`from`, id1, `to`, id2) VALUES (%s, %s, %s, %s)", \
                    [(theDict[link[0]], link[0], theDict[link[1]], link[1]) for link in theList])
    
    cur.close()
    conn.close()
    print("Upload to SQL successful...")

def _spend_time(start_time):
    totle_time = round(time.time()-start_time, 0)
    _min, _sec = divmod(totle_time, 60)
    _hr, _min = divmod(_min, 60)
    print('Time: {}h {}m {}s'.format(int(_hr), int(_min), int(_sec)))


friends_info_set = set() #基本資料
friends_link_list = list() #關係資料
main()

