# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 18:50:01 2018

@author: mars
"""

from selenium import webdriver
import time
#import getpass
#import re
#import csv
import re


#FJU 2-hand scrape
def main():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2} #關閉chrome通知提醒
    chrome_options.add_experimental_option("prefs",prefs)

    chromePath = '/Users/mars/Desktop/Report#Data/Python/Crawler/chromedriver' #chromedriver path
    driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)
    driver.get('https://www.facebook.com')
    
    _login(driver) #登入FB
    
    fju_2hand_href = "https://www.facebook.com/groups/458946517501034/"
    _check_keyword(driver, fju_2hand_href) #檢查關鍵字
    
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

def _check_keyword(driver, href, keyword="", count=0, ceiling=1, interval=5):
    driver.get(href)
    
    if count == 0:
        keyword = input("input keyword: ")
        keyword = re.split("\W+\s?", keyword) #以非文字為分割條件
        #print(keyword)
        driver.find_element_by_link_text("最相關貼文").click() #人氣貼文
        driver.find_element_by_xpath("//a[@class='_54nc']").click() #切換最新動態
        print("Switch to lastest news page...\n-------------------------------")
    
    time.sleep(5)
    article_context = driver.find_elements_by_xpath("//div[@role='region']/div[@role='feed']/div[@role='article']/div/div/div[@class='_1dwg _1w_m _q7o']")
    for context in article_context:
        for key in keyword:
            if re.search(key, context.text):
                print(context.text, "\n---------------------------------------------------------")
                count = ceiling
        
    if count < ceiling:
        time.sleep(interval)
        _check_keyword(driver, href, keyword, count+1)

#def _send_mail():
    

main()

