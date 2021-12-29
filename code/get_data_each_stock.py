# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 15:05:25 2021

@author: anshu
"""
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

def get_data_from_webpage(driver,elm,stock_list):    
    
    # get the webpage
    driver.get(elm)
    time.sleep(2)
    
    #click to get table
    try:
        driver.find_element_by_css_selector('a[class="estimate-bar__button"]').click()
        time.sleep(2)
    except:
        print("okay")
    
    # get the name of result sheet
    name = driver.find_element_by_css_selector('h1[class="release-header-information-title"]').text
    name = name.replace(" ","")
    
    # save the name of company and link in the stock_list
    stock_list.append({'name':name, 'link':elm})
    
    # create dataframe
    res_df = pd.DataFrame()
    
    # get column names from top row
    row = driver.find_element_by_css_selector('tr[class="multiform-tr-qtrs"]')
    cols = row.find_elements_by_css_selector('td[class="multiform-td-qtr"]')
    col_names = []
    for col in cols:
        col_names.append(col.text)
    
    # get estimize value and count columns
    row = driver.find_element_by_css_selector('tr[class="multiform-tr-consensus multiform-tr-estimize"]')
    cols = row.find_elements_by_css_selector('td[class="multiform-td-data"]')
    est_val_dict = {}
    est_cnt_dict = {}
    i=0
    for col in cols:
        tmp = col.text.split()
        try:
            est_val_dict[col_names[i]] = tmp[0]
        except:
            est_val_dict[col_names[i]] = np.nan
        try:
            est_cnt_dict[col_names[i]] = tmp[1]
        except:
            est_cnt_dict[col_names[i]] = np.nan
        i=i+1
    est_val_df = pd.DataFrame([est_val_dict])
    est_cnt_df = pd.DataFrame([est_cnt_dict])
    res_df = pd.concat([res_df,est_val_df],ignore_index=True)
    res_df = pd.concat([res_df,est_cnt_df],ignore_index=True)
    
    # get wall street columns
    row = driver.find_element_by_css_selector('tr[class="multiform-tr-consensus multiform-tr-wallstreet"]')
    cols = row.find_elements_by_css_selector('td[class="multiform-td-data"]')
    wall_st_dict = {}
    i=0
    for col in cols:
        wall_st_dict[col_names[i]] = col.text
        i=i+1
    wall_st_df = pd.DataFrame([wall_st_dict])
    res_df = pd.concat([res_df,wall_st_df],ignore_index=True)
    
    # print("res: ",res_df)
    
    # get actual values columns
    row = driver.find_element_by_css_selector('tr[class="multiform-tr-actuals"]')
    cols = row.find_elements_by_css_selector('td[class="multiform-td-data"]')
    act_val_dict = {}
    act_gth_dict = {}
    i=0
    for col in cols:
        tmp = col.text.split()
        act_val_dict[col_names[i]] = tmp[0]
        act_gth_dict[col_names[i]] = tmp[1]
        i=i+1
    act_val_df = pd.DataFrame([act_val_dict])
    res_df = pd.concat([res_df, act_val_df],ignore_index=True)
    act_gth_df = pd.DataFrame([act_gth_dict])
    res_df = pd.concat([res_df, act_gth_df],ignore_index=True)
    
    # quit driver
    # driver.close()
    # print("res: ",res_df)
    
    # save dataframe
    res_df.to_csv('../output/' + name + '.csv')
    
    return stock_list