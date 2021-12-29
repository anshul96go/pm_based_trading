# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 23:04:16 2021

@author: anshu
"""

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
from helper_get_final_sheet import *
import time

def extract_earning_dates(stk):
    earning_hist = si.get_earnings_history(stk)
    earning_hist_df = pd.DataFrame(earning_hist)
    
    earning_hist_df['date'] = earning_hist_df.startdatetime.str[:10]
    earning_hist_df = earning_hist_df.drop_duplicates(subset=['date'])
    
    ### 4.3 drop the future eps dates
    earning_hist_df = earning_hist_df.dropna(subset=['epsactual'])
    earning_hist_df.to_csv('../earning_dates_data/earning_'+stk+'.csv') 


try:
    completed_df = pd.read_csv('../records/earning_date_status.csv')
except:
    stk = 'CROX'
    extract_earning_dates(stk)
    completed_list = [{'name':stk,'last_extract':datetime.datetime.today().strftime('%m-%d-%Y')}]
    completed_df = pd.DataFrame(completed_list)
    completed_df.to_csv('../records/hist_data_status.csv')
    
hit_df = pd.read_csv('../output/stock_hit_rate.csv')
stock_list_full = list(set(list(hit_df['name'])))
stock_list_completed = list(set(list(completed_df['name'])))
stock_list = list(set(stock_list_full) - set(stock_list_completed)) 


for stk in stock_list:
    extract_earning_dates(stk)  
    tmp_df = pd.DataFrame([{'name':stk,'last_extract':datetime.datetime.today().strftime('%m-%d-%Y')}])
    completed_df = pd.concat([completed_df,tmp_df],ignore_index=True)
    completed_df.to_csv('../records/earning_date_status.csv')

