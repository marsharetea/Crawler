# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 08:56:52 2018

@author: user
"""


from selenium import webdriver
import time
#import getpass
import re
import csv


#IG profile test
def main(): 
    start_time = time.time()
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2} #關閉chrome通知提醒
    chrome_options.add_experimental_option("prefs",prefs)

    chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver' #chromedriver path
    driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)
    driver.get('https://www.instagram.com/')
    
    _login(driver) #登入FB
    
    global follow_info_list #基本資料
    global follow_link_list #關係資料
    global posts_set #post file
    global tags_dict #tag file
    
    time.sleep(2)
    profile_href = driver.find_element_by_xpath('//a[@class="_8scx2 _gvoze coreSpriteDesktopNavProfile"]').get_attribute('href') #個人頁面網址
    _scrpae_personal_file(driver, profile_href) #深度遞迴截取
    
    follow_info_indexed = _indexed_info(follow_info_list) #編列索引
    
    _eliminate_duplication_link(follow_link_list) #刪除重複連結
    
    try:
        del tags_dict[''] #刪除Null key
        _del_len1_tag() #刪除長度為 1的tag或單詞
    except:
        print('Ｎot null value!')
        
    tags_sorted_list = _tag_count_sort(tags_dict) #以tag次數降冪排序
    
    _convert_to_csv(follow_info_indexed, follow_info_list, follow_link_list, tags_sorted_list) #輸出成csv檔
    
    driver.close()
        
    _spend_time(start_time) #花費時間

def _login(driver):
    #account = input('input your account:')
    #passwd = getpass.getpass("input your password:")
    account = "marsharetea"
    passwd = 'puo0534'
    
    try:
        time.sleep(1)
        driver.find_element_by_link_text('登入').click()
    except:
        time.sleep(2)
        driver.find_element_by_link_text('登入').click()
    
    time.sleep(1)
    driver.find_element_by_name("username").clear() #清除欄位
    driver.find_element_by_name("username").send_keys(account) #輸入帳號
    print('Account entered...')
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(passwd) #輸入密碼
    print('Password entered...')
    driver.find_element_by_xpath('//span[@class="_t38eb _ov9ai"]/button').click() #按下登入

def _scrpae_personal_file(driver, href, count=0, depth=1):
    driver.get(href)
    
    time.sleep(1)
    profile_account_now = driver.find_element_by_xpath('//div[@class="_ienqf"]/h1').text #用戶帳號
    try:
        profile_name_now = driver.find_element_by_xpath('//div[@class="_tb97a"]/h1').text #用戶名稱
    except:
        profile_name_now = ''
    
    if count is 0:
        follow_info_list.append([profile_account_now, profile_name_now])
    print('User account: {} \nUser name: {} \n--------------------------'.format(profile_account_now, profile_name_now))
    
    profile_info_column = driver.find_elements_by_class_name('_t98z6') #posts, followers, following
    
    follow_href_cache_list = _scrape_follow(driver, profile_info_column, profile_account_now, profile_name_now) #擷取所有粉絲&追蹤人
    
    #_scrape_all_post(driver) #擷取所有post

    if count+1 < depth:
        for href in follow_href_cache_list:
            _scrpae_personal_file(driver, href, count+1)
    else:
        return

def _scrape_follow(driver, info_column, account_now, name_now):
    follow_href_cache_list = [] #暫存follow href
    for i in range(1, len(info_column)):
        if info_column[i].tag_name is 'a': #<span> is not public
            info_column[i].click() #user 1:followers 2:followings
            
            time.sleep(1)
            _scroll_to_bottom_follow(driver)
            
            follows_elem = driver.find_elements_by_xpath('//div[@class="_pfyik"]/div/div/div/ul/div/li/div/div/div/div/a') #follows 帳號&網址
            follows_name = driver.find_elements_by_xpath('//div[@class="_pfyik"]/div/div/div/ul/div/li/div/div/div/div[@class="_9mmn5"]') #follows 名稱

            for j in range(len(follows_elem)):
                if follows_elem[j].text not in [info[0] for info in follow_info_list]:
                    follow_href_cache_list.append(follows_elem[j].get_attribute('href'))
                    follow_info_list.append([follows_elem[j].text, follows_name[j].text])
                    if i is 1: #follower
                        follow_link_list.append([follows_elem[j].text, account_now])
                    else: #following
                        follow_link_list.append([account_now, follows_elem[j].text])

            driver.find_element_by_xpath('//div[@class="_pfyik"]/button').click() #關閉follow
    return follow_href_cache_list

def _scrape_all_post(driver):
    for i in range(1):
    #while _scroll_to_bottom_post(driver):
        profile_posts = driver.find_elements_by_xpath('//div[@class="_6d3hm _mnav9"]/div/a/div/div/img') #目前頁面所有post
        for post in [post.get_attribute('alt') for post in profile_posts]:
            if post not in posts_set:
                posts_set.add(post)
                tags = _check_separator(post) #post內容以 "#,-,\n,，"隔開
                _input_tag_to_dict(tags) #加入字典裡並計算次數

def _scroll_to_bottom_follow(driver):
    scroll_pause_time = 1

    # Get scroll height
    last_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')

    while True:
        # Scroll down to bottom
        driver.execute_script('document.getElementsByClassName("_gs38e")[0].scrollTo(0, document.getElementsByClassName("_gs38e")[0].scrollHeight);')

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script('return document.getElementsByClassName("_gs38e")[0].scrollHeight')
        if new_height == last_height:
            return
        last_height = new_height

def _scroll_to_bottom_post(driver):
    scroll_pause_time = 1
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    scroll_count = 0
    while scroll_count < 1:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Calculate new scroll height and compare with last scroll height
        if new_height != last_height:
            return True
        else:
            print('Stop scroll down...')
            return False
        scroll_count += 1

def _check_separator(post):
    tags = re.split('#| |\n|–|，', post)
    return tags

def _input_tag_to_dict(tagList):
    for tag in tagList:
        if tag in tags_dict:
            tags_dict[tag] += 1
        else:
            tags_dict[tag] = 1

def _del_len1_tag():
    len1_tag = []
    for tag in tags_dict:
        if len(tag) is 1:
            len1_tag.append(tag)
    for tag in len1_tag:
        del tags_dict[tag]

def _tag_count_sort(theDict):
    theList = [[value, key] for key, value in theDict.items()]
    theList.sort(reverse=True)
    return theList

def _indexed_info(theList):
    theDict_indexed = {}
    for i in range(len(theList)):
        theDict_indexed[theList[i][0]] = i+1
    print('Indexed information...')
    return theDict_indexed

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

def _convert_to_csv(indexDict, infoList, linkList, tagList=0):
    csvFile = open('/Users/mars/Desktop/IG_follow_info.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(('id', 'account', 'name'))
        for info in infoList:
            writer.writerow((indexDict[info[0]], info[0], info[1]))
    finally:
        csvFile.close()
    
    csvFile = open('/Users/mars/Desktop/IG_follow_link.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(('from', 'id1', 'to', 'id2'))
        for link in linkList:
            writer.writerow([indexDict[link[0]], link[0], indexDict[link[1]], link[1]])
    finally:
        csvFile.close()
    
    csvFile = open('/Users/mars/Desktop/IG_profile_tag.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(('count', 'tag'))
        for row in tagList:
            writer.writerow(row)
    finally:
        csvFile.close()
    print('Loadfile...')
    
def _spend_time(start_time):
    totle_time = round(time.time()-start_time, 0)
    _min, _sec = divmod(totle_time, 60)
    _hr, _min = divmod(_min, 60)
    print('Time: {}h {}m {}s'.format(int(_hr), int(_min), int(_sec)))


follow_info_list = list() #基本資料
follow_link_list = list() #關係資料
posts_set = set() #post file
tags_dict = {} #tag file
main()

