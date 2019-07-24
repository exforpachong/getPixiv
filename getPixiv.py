import numpy as np ,pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import re
import requests
import os
import pyautogui

searchPath = '//*[@id="js-react-search-mid"]/div/div[%s]/figure/div/a/div' #range(1,41)
searchInPath = '//*[@id="root"]/div[1]/div/div/main/section/div[1]/div/figure/div/div/div/a/img'

huashiPath = '//*[@id="root"]/div[1]/div/div[2]/div[1]/div/ul/li[%s]/div/div/div/a/div[2]' #range(1,49)
huashiInPath = '//*[@id="root"]/div[1]/div/div/main/section/div[1]/div/figure/div/div/div/a/div/img'


newPath = '/html/body/div[5]/div/div/div/img'

waitSecond = 30   #这里设置载入一个页面等待页面响应的最大时间

def init_browser():   #初始化浏览器的函数，该函数的作用是配置请求的用户浏览器信息，以及用户信息
    chromeOptions = webdriver.ChromeOptions()
    # 设置代理
    # chromeOptions.add_argument("--proxy-server=http://121.233.207.225:9999")  #这里注释因为没有花钱买代理ip
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    user_data = 'H:/github/qichacha/User Data'  # 这里面填你的user data对应的文件夹
    # user_agent = random.choice(agents)  #有些服务器需多次登录需要设置不同用户浏览器信息来反爬虫
    chromeOptions.add_argument('user-agent=%s' % user_agent)
    chromeOptions.add_argument('--user-data-dir=%s' % user_data)
    # chromeOptions.add_argument('Cookie=%s'% cookie)    #这一块没有搞懂，cookie还是不会设置，所以前面通过配置user_data信息来达到同样效果
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    return browser

def SavePicAny(b,t):
    time.sleep(t)
    b.implicitly_wait(t)  # 浏览器等待
    pyautogui.hotkey('alt', 's')  # 保存图片

def save_pic_by_bro(browser,huashi=False):

    SavePicAny(browser, 1)  # 到处调用！防止出错！

    if huashi:
        thePath = searchInPath  # 都一样？
    else:
        thePath = searchInPath
    WebDriverWait(browser, waitSecond, 0.5).until(
        EC.presence_of_element_located((By.XPATH, thePath)))

    #测试的
    SavePicAny(browser, 1)  # 到处调用！防止出错！
    browser.find_element_by_xpath(thePath).click()
    WebDriverWait(browser, waitSecond, 0.5).until(
        EC.presence_of_element_located((By.XPATH, newPath)))
    img = browser.find_element_by_xpath(newPath)

    #原来的
    # img = browser.find_element_by_xpath(thePath)

    SavePicAny(browser, 1)  # 到处调用！防止出错！

    ActionChains(browser).context_click(img).perform()
    time.sleep(1)
    pyautogui.typewrite(['down', 'down', 'enter', 'enter'])
    # pyautogui.typewrite(['down', 'down', 'down', 'down', 'down', 'down', 'down', 'enter','enter'])
    # pyautogui.typewrite('v')  #不要用快捷键保存，上面的好用！

    SavePicAny(browser,1)   #到处调用！防止出错！

def save_from_Oneurl(url,huashi=False):   #根据输入的url页面来保存当前页面下所有的图片，huashi=True，说明是画师页面，False说明是搜索页面
    browser = init_browser()  #初始化浏览器，配置请求的用户浏览器信息，以及用户信息
    time.sleep(10)  #打开浏览器的瞬间需要手动连接vpn，所以等待了10s，主要手速要快，否则这里设置时间长一点！
    browser.get(url)  #进入主页
    b = 41   #搜索页面每页存了41张图片
    if huashi:
        b = 49  #画师每个页面存了48张图片
    i = 1  #初始保存图片的数值
    ExceptionNum = 1   #图片保存异常的次数，后面设置尝试3次不成功就跳过这张图片，因为有时候不是图片，是gif格式……
    while i < b:

        SavePicAny(browser, 1)  # 到处调用！防止出错！

        print('Begin to save the number %s pic'% str(i))
        if huashi:
            strToChoose = huashiPath % str(i)   #画师页面单张图片的XPath
        else:
            strToChoose = searchPath % str(i)   #搜索页面单张图片的XPath
        try:
            WebDriverWait(browser, waitSecond, 0.5).until(EC.presence_of_element_located((By.XPATH, strToChoose)))  #寻找图片
            browser.find_element_by_xpath(strToChoose).click()  #点击该张图片
            # 进入保存图片的页面，开始保存

            SavePicAny(browser, 1)  # 到处调用！防止出错！

            save_pic_by_bro(browser,huashi)
        except Exception as e:
            browser.get(url)  #出现异常，从新得到原来的网址
            ExceptionNum += 1  #出现异常则异常次数加一
            if ExceptionNum >=3:  #如果保存同一张图片的异常次数超过3次，则放弃本张图片的保存
                print('the picture of number %s has not saved!' % str(i))
                ExceptionNum = 1  #放弃时异常次数要重置为1
                i = i + 1
                continue
            else:
                continue
        browser.back()   #保存成功，浏览器回退到主页面
        ExceptionNum = 1  #正常保存时异常次数也要重置为1
        i = i + 1

        SavePicAny(browser, 1)  # 到处调用！防止出错！
    SavePicAny(browser, 1)  # 到处调用！防止出错！

# def get_new_url(name):
#     root_url='https://www.pixiv.net/'
#     browser = init_browser()
#     browser.get(root_url)
#     browser.find_element_by_xpath('//*[@id="suggest-input"]').send_keys(name)
#     browser.find_element_by_xpath('//*[@id="suggest-container"]/input[2]').click()
#     time.sleep(150)

if __name__ == '__main__':
    # get_new_url('折纸')
    # save_from_Oneurl('https://www.pixiv.net/member_illust.php?id=73152', True)
    save_from_Oneurl('https://www.pixiv.net/member_illust.php?id=73152&p=3',True)
    print('save finished!')
    time.sleep(5)
    #test