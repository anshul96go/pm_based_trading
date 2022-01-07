# 1. Import packages
import pandas as pd
import numpy as np
import re
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

import time
import os
import bs4 as bs
import urllib.request
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from selenium.webdriver.common.proxy import Proxy, ProxyType
import re
import random
import pyautogui as py

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from get_data_each_stock import *

# 2. Open browser
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

### create config from proxy
def create_proxy_config(proxy):
    myProxy = proxy
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'ftpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': '' # set this value as desired
        })
    return proxy

proxies = get_proxies()
proxies = get_proxies()
if len(proxies) ==0:
    proxy = None
    proxy_pool = None
else:
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)
    proxy = create_proxy_config(proxy)

def open_browser(proxy,proxy_pool):
    try:
        driver = webdriver.Firefox(executable_path=r'C:/Users/anshu/Downloads/geckodriver.exe',proxy=proxy)
    except:
        if len(proxy_pool)==0:
            proxy=None
        else:
            proxy = next(proxy_pool)
            proxy = create_proxy_config(proxy)
            driver = webdriver.Firefox(executable_path=r'C:/Users/anshu/Downloads/geckodriver.exe',proxy=proxy)
    time.sleep(2)
    return driver,proxy,proxy_pool



# initialise stock list
stock_list = []

# # open Consumer Durable webpage
# driver, proxy,proxy_pool = open_browser(proxy,proxy_pool)
# driver.get('https://www.estimize.com/sectors/consumer-discretionary')

# # click to get all stocks list
# driver.find_element_by_css_selector('div[class="pagination-footer').click()
# time.sleep(2)

# # append list of links
# elm_list = []
# for elm in driver.find_elements_by_css_selector('a[class="linked-row closed'):
#     elm = elm.get_attribute('href')
#     elm = (elm[:-9])
#     elm_list.append(elm)

# if len(elm_list)==0:
#     print("using opened one now")
#     for elm in driver.find_elements_by_css_selector('a[class="linked-row opened'):
#         elm = elm.get_attribute('href')
#         elm = (elm[:-9])
#         elm_list.append(elm) 

# # click href link    
# for elm in elm_list:    
#     print(elm)
#     try:
#         stock_list = get_data_from_webpage_2(driver,elm,stock_list)
#     except:
#         continue

# # save the stock_list as df
# tmp_df = pd.DataFrame(stock_list)
# tmp_df.to_csv('../output/stock_list_2.csv') 


def get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = 'https://www.estimize.com/sectors/consumer-discretionary',op_file='stock_list_2.csv'):
    # initiate stock_list
    stock_list = []
    
    # open Consumer Durable webpage
    driver, proxy,proxy_pool = open_browser(proxy,proxy_pool)
    driver.get(ind_link)
    
    # click to get all stocks list
    driver.find_element_by_css_selector('div[class="pagination-footer').click()
    time.sleep(2)
    
    # append list of links
    elm_list = []
    for elm in driver.find_elements_by_css_selector('a[class="linked-row closed'):
        elm = elm.get_attribute('href')
        elm = (elm[:-9])
        elm_list.append(elm)
    
    if len(elm_list)==0:
        print("using opened one now")
        for elm in driver.find_elements_by_css_selector('a[class="linked-row opened'):
            elm = elm.get_attribute('href')
            elm = (elm[:-9])
            elm_list.append(elm) 
    
    # click href link    
    for elm in elm_list:    
        print(elm)
        try:
            stock_list = get_data_from_webpage_2(driver,elm,stock_list)
        except:
            continue
    
    # save the stock_list as df
    res_df = pd.read_csv('../output/'+op_file)
    tmp_df = pd.DataFrame(stock_list)
    res_df = pd.concat([res_df,tmp_df],)
    res_df.to_csv('../output/'+op_file)
    return    

# consumer discretionary
lnk = 'https://www.estimize.com/sectors/consumer-discretionary'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# consumer staple
lnk = 'https://www.estimize.com/sectors/consumer-staples'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# energy
lnk = 'https://www.estimize.com/sectors/energy'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# financials
lnk = 'https://www.estimize.com/sectors/financials'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# healthcare
lnk = 'https://www.estimize.com/sectors/health-care'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# industrials
lnk = 'https://www.estimize.com/sectors/industrials'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# it
lnk = 'https://www.estimize.com/sectors/information-technology'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# materials
lnk = 'https://www.estimize.com/sectors/materials'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# telecom
lnk = 'https://www.estimize.com/sectors/telecommunication-services'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')

# utilities
lnk = 'https://www.estimize.com/sectors/utilities'
get_est_file_stock_list(driver,proxy,proxy_pool,ind_link = lnk,op_file='stock_list_2.csv')