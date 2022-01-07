# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 22:19:50 2021

@author: anshu
"""

import yfinance as yf
import pandas as pd
import numpy as np
import yahoo_fin.stock_info as si
import datetime
from pandas.tseries.offsets import BDay
import time

def extract_hist_data(stk,period="900d"):
    stock = yf.Ticker(stk)
    data = stock.history(period=period)
    data.to_csv('../hist_data/'+stk+'_'+period+'.csv')

try:
    completed_df = pd.read_csv('../records/hist_data_status.csv')
except:
    stk = 'CROX'
    period="2000d"
    extract_hist_data(stk,period=period)
    completed_list = [{'name':stk,'period':period,'last_extract':datetime.datetime.today().strftime('%m-%d-%Y')}]
    completed_df = pd.DataFrame(completed_list)
    completed_df.to_csv('../records/hist_data_status.csv')
    
hit_df = pd.read_csv('../output/stock_hit_rate.csv')
stock_list_full = list(set(list(hit_df['name'])))
stock_list_completed = list(set(list(completed_df['name'])))
stock_list = list(set(stock_list_full) - set(stock_list_completed)) 
print(len(stock_list_full),len(stock_list_completed),len(stock_list))    

while(len(stock_list)>0):
    try:
        for stk in stock_list:
            print(stk)
            period="2000d"
            extract_hist_data(stk,period=period)  
            tmp_df = pd.DataFrame([{'name':stk,'period':period,'last_extract':datetime.datetime.today().strftime('%m-%d-%Y')}])
            completed_df = pd.concat([completed_df,tmp_df],ignore_index=True)
            completed_df.to_csv('../records/hist_data_status.csv')
            time.sleep(1)
    except:
        hit_df = pd.read_csv('../output/stock_hit_rate.csv')
        stock_list_full = list(set(list(hit_df['name'])))
        stock_list_completed = list(set(list(completed_df['name'])))
        stock_list = list(set(stock_list_full) - set(stock_list_completed)) 
        print(len(stock_list_full),len(stock_list_completed),len(stock_list)) 
