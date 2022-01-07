# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:06:22 2021

@author: anshu
"""
import yfinance as yf
import pandas as pd
import numpy as np
import yahoo_fin.stock_info as si
import datetime
from pandas.tseries.offsets import BDay


def extract_hist_data(stk,period="900d"):
    stock = yf.Ticker(stk)
    data = stock.history(period=period)
    data.to_csv('../hist_data/'+stk+'_'+period+'.csv')

def get_past_earning_dates(stk):
    # earning_hist = si.get_earnings_history(stk)
    # earning_hist_df = pd.DataFrame(earning_hist)
    # print(earning_hist_df)
    # earning_hist_df.to_csv('../output/earning_data.csv')
    earning_hist_df = pd.read_csv('../earning_dates_data/earning_'+stk+'.csv')
    
    ### 4.2 drop duplicate dates
    earning_hist_df['date'] = earning_hist_df.startdatetime.str[:10]
    earning_hist_df = earning_hist_df.drop_duplicates(subset=['date'])
    
    ### 4.3 drop the future eps dates
    earning_hist_df = earning_hist_df.dropna(subset=['epsactual'])
    # print(earning_hist_df)
    # earning_hist_df.to_csv('../output/earning_data_upd.csv')
    # print('earning_hist_df: ',earning_hist_df)
    dates = [x[:10] for x in list(earning_hist_df.iloc[:8]['date'])]
    dates = dates[::-1]
    return dates

def get_estimize_data(stk,dates):
    # print('dates: ',dates)
    est_df = pd.read_csv('../output/'+stk+'.csv').T
    est_df = est_df.iloc[1:]
    # print('est_df: ',est_df)
    est_df.columns = ['est_val','est_cnt','wl_st','act','yoy']
    est_df['date'] = dates
    for col in ['est_val','est_cnt','wl_st','act']:
        est_df[col] = est_df[col].astype(float)
    return est_df

def get_qtr_earn_stats(est_df,data):
    # initialise metrics
    count_no_signal,count_no_data = 0,0
    success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op = 0,0,0,0
    pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op = [],[],[],[]        
 
    # iterate over each quarter
    for i in range(len(est_df)):
        ### get historical data for earning day and 1 day prior 
        dt = est_df.iloc[i]['date']
        
        try:
            idx = data[data['Date']==dt].index[0]
            
        except:
            print('dt: ',dt)
            print('hist data not exist')
            continue
        # tmp = data.loc[data.index.isin([idx-1,idx])]
        # tmp = tmp.reset_index()
        # del tmp['index']
        # print(tmp)
    return
        
    
    # ### 6.2 declare variables for t-1 data points
    #     cl_t0 = tmp.iloc[0]['Close']
    #     op_t0 = tmp.iloc[0]['Open']
    #     hh_t0 = tmp.iloc[0]['High']
    #     lw_t0 = tmp.iloc[0]['Low']
    #     vl_t0 = tmp.iloc[0]['Volume']
    
    #     ### 6.3 declare variables for t data points
    #     cl_t1 = tmp.iloc[1]['Close']
    #     op_t1 = tmp.iloc[1]['Open']
    #     hh_t1 = tmp.iloc[1]['High']
    #     lw_t1 = tmp.iloc[1]['Low']
    #     vl_t1 = tmp.iloc[1]['Volume']
        
    #     ### 6.4 get estimize signal based on wall street and estimize estimate
    #     est_signal = 0
    #     if pd.isna(est_df.iloc[i]['est_val']):
    #         est_signal = 0
    #         count_no_signal+=1    
    #     elif est_df.iloc[i]['est_val'] > est_df.iloc[i]['wl_st']:
    #         est_signal = 1
    #     elif est_df.iloc[i]['est_val'] < est_df.iloc[i]['wl_st']:
    #         est_signal = -1
    #     else:
    #         est_signal = 0
    #         count_no_signal+=1
            
    #     ### 6.5 check for success based on bull signal
    #     if est_signal == 1:
    #         # estimate pnl for each enter-exit option
    #         pnl_pct_cl_cl.append(round((cl_t0-cl_t1)*100/cl_t1,2))
    #         pnl_pct_op_op.append(round((op_t0-op_t1)*100/op_t1,2))
    #         pnl_pct_op_cl.append(round((cl_t0-op_t1)*100/op_t1,2))
    #         pnl_pct_cl_op.append(round((op_t0-cl_t1)*100/cl_t1,2))
            
    #         # check for close to close success
    #         if cl_t1<cl_t0:
    #             success_count_cl_cl+=1   
    #         # check for open to open success
    #         if op_t1<op_t0:
    #             success_count_op_op+=1
    #         # check for open to close success
    #         if op_t1<cl_t0:
    #             success_count_op_cl+=1
    #         # check for close to open success
    #         if cl_t1<op_t0:
    #             success_count_cl_op+=1
        
    #     ### 6.6 check for success based on bear signal
    #     elif est_signal == -1:
            
    #         # estimate pnl for each enter-exit option
    #         pnl_pct_cl_cl.append(round(-(cl_t0-cl_t1)*100/cl_t1,2))
    #         pnl_pct_op_op.append(round(-(op_t0-op_t1)*100/op_t1,2))
    #         pnl_pct_op_cl.append(round(-(cl_t0-op_t1)*100/op_t1,2))
    #         pnl_pct_cl_op.append(round(-(op_t0-cl_t1)*100/cl_t1,2))        
            
    #         # check for close to close success
    #         if cl_t1>cl_t0:
    #             success_count_cl_cl+=1        
    #         # check for open to open success
    #         if op_t1>op_t0:
    #             success_count_op_op+=1
    #         # check for open to close success
    #         if op_t1>cl_t0:
    #             success_count_op_cl+=1
    #         # check for close to open success
    #         if cl_t1>op_t0:
    #             success_count_cl_op+=1
        
    #     # check for no signal
    #     else:
    #         # do nothing
    #         success_count_cl_cl += 0 
    
    # return success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op