# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 15:08:21 2021

@author: anshu
"""
# 0. import package
import yfinance as yf
import pandas as pd
import numpy as np
import yahoo_fin.stock_info as si
import datetime
from pandas.tseries.offsets import BDay

def get_qtr_earn_stats_trial(est_df,data):
    # initialise metrics
    count_no_signal,count_no_data = 0,0
    success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op = 0,0,0,0
    pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op = [],[],[],[]        
 
    # iterate over each quarter
    for i in range(len(est_df)):
        
        # get historical data for earning day and 1 day prior 
        dt = est_df.iloc[i]['date']
        
        # check if the historcial data exist for the date and 
        # increase the count_no_data if it doesn't exist
        try:
            idx = data[data['Date']==dt].index[0]
            
        except:
            # print('hist data not available for date: ',dt)
            count_no_data+=1
            continue
        
        # slice the historic data and reverse the dataframe for latest value on top
        tmp = data.loc[data .index.isin([idx-1,idx])]
        tmp = tmp.reindex(index=tmp.index[::-1])
        tmp = tmp.reset_index()
        del tmp['index']
        # print(tmp)
        
    ### 6.2 declare variables for t-1 data points
        cl_t0 = tmp.iloc[0]['Close']
        op_t0 = tmp.iloc[0]['Open']
        hh_t0 = tmp.iloc[0]['High']
        lw_t0 = tmp.iloc[0]['Low']
        vl_t0 = tmp.iloc[0]['Volume']
    
        ### 6.3 declare variables for t data points
        cl_t1 = tmp.iloc[1]['Close']
        op_t1 = tmp.iloc[1]['Open']
        hh_t1 = tmp.iloc[1]['High']
        lw_t1 = tmp.iloc[1]['Low']
        vl_t1 = tmp.iloc[1]['Volume']
        
        ### 6.4 get estimize signal based on wall street and estimize estimate
        est_signal = 0
        # print((est_df.iloc[i]))
        if pd.isna(est_df.iloc[i]['est_val']):
            est_signal = 0
            count_no_signal+=1    
        elif est_df.iloc[i]['est_val'] > est_df.iloc[i]['wl_st']:
            est_signal = 1
        elif est_df.iloc[i]['est_val'] < est_df.iloc[i]['wl_st']:
            est_signal = -1
        else:
            est_signal = 0
            count_no_signal+=1
        # print("signal: ",est_signal)
        # print("opening prices: ",op_t0,op_t1)
        # print("op_op profit: ",est_signal*round((op_t0-op_t1)*100/op_t1,2))
        
        ### 6.5 check for success based on bull signal
        if est_signal == 1:
            # estimate pnl for each enter-exit option
            pnl_pct_cl_cl.append(round((cl_t0-cl_t1)*100/cl_t1,2))
            pnl_pct_op_op.append(round((op_t0-op_t1)*100/op_t1,2))
            pnl_pct_op_cl.append(round((cl_t0-op_t1)*100/op_t1,2))
            pnl_pct_cl_op.append(round((op_t0-cl_t1)*100/cl_t1,2))
            
            # check for close to close success
            if cl_t1<cl_t0:
                success_count_cl_cl+=1   
            # check for open to open success
            if op_t1<op_t0:
                success_count_op_op+=1
            # check for open to close success
            if op_t1<cl_t0:
                success_count_op_cl+=1
            # check for close to open success
            if cl_t1<op_t0:
                success_count_cl_op+=1
        
        ### 6.6 check for success based on bear signal
        elif est_signal == -1:
            
            # estimate pnl for each enter-exit option
            pnl_pct_cl_cl.append(round(-(cl_t0-cl_t1)*100/cl_t1,2))
            pnl_pct_op_op.append(round(-(op_t0-op_t1)*100/op_t1,2))
            pnl_pct_op_cl.append(round(-(cl_t0-op_t1)*100/op_t1,2))
            pnl_pct_cl_op.append(round(-(op_t0-cl_t1)*100/cl_t1,2))        
            
            # check for close to close success
            if cl_t1>cl_t0:
                success_count_cl_cl+=1        
            # check for open to open success
            if op_t1>op_t0:
                success_count_op_op+=1
            # check for open to close success
            if op_t1>cl_t0:
                success_count_op_cl+=1
            # check for close to open success
            if cl_t1>op_t0:
                success_count_cl_op+=1
        
        # check for no signal
        else:
            # do nothing
            success_count_cl_cl += 0 
    
    return count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op


def get_qtr_earn_stats_trial_amc(est_df,data):
    # initialise metrics
    count_no_signal,count_no_data = 0,0
    success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op = 0,0,0,0
    pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op = [],[],[],[]        
 
    # iterate over each quarter
    for i in range(len(est_df)):
        
        # get historical data for earning day and 1 day prior 
        dt = est_df.iloc[i]['date']
        
        # check if the historcial data exist for the date and 
        # increase the count_no_data if it doesn't exist
        try:
            idx = data[data['Date']==dt].index[0]
            
        except:
            # print('hist data not available for date: ',dt)
            count_no_data+=1
            continue
        
        # slice the historic data and reverse the dataframe for latest value on top
        tmp = data.loc[data .index.isin([idx,idx+1])]
        tmp = tmp.reindex(index=tmp.index[::-1])
        tmp = tmp.reset_index()
        del tmp['index']
        # print("date based data: ",tmp)
        
    ### 6.2 declare variables for t-1 data points
        cl_t0 = tmp.iloc[0]['Close']
        op_t0 = tmp.iloc[0]['Open']
        hh_t0 = tmp.iloc[0]['High']
        lw_t0 = tmp.iloc[0]['Low']
        vl_t0 = tmp.iloc[0]['Volume']
    
        ### 6.3 declare variables for t data points
        cl_t1 = tmp.iloc[1]['Close']
        op_t1 = tmp.iloc[1]['Open']
        hh_t1 = tmp.iloc[1]['High']
        lw_t1 = tmp.iloc[1]['Low']
        vl_t1 = tmp.iloc[1]['Volume']
        
        ### 6.4 get estimize signal based on wall street and estimize estimate
        est_signal = 0
        # print((est_df.iloc[i]))
        if pd.isna(est_df.iloc[i]['est_val']):
            est_signal = 0
            count_no_signal+=1    
        elif est_df.iloc[i]['est_val'] > est_df.iloc[i]['wl_st']:
            est_signal = 1
        elif est_df.iloc[i]['est_val'] < est_df.iloc[i]['wl_st']:
            est_signal = -1
        else:
            est_signal = 0
            count_no_signal+=1
        # print("signal: ",est_signal)
        # print("opening prices: ",op_t0,op_t1)
        # print("op_op profit: ",est_signal*round((op_t0-op_t1)*100/op_t1,2))
        
        ### 6.5 check for success based on bull signal
        if est_signal == 1:
            # estimate pnl for each enter-exit option
            pnl_pct_cl_cl.append(round((cl_t0-cl_t1)*100/cl_t1,2))
            pnl_pct_op_op.append(round((op_t0-op_t1)*100/op_t1,2))
            pnl_pct_op_cl.append(round((cl_t0-op_t1)*100/op_t1,2))
            pnl_pct_cl_op.append(round((op_t0-cl_t1)*100/cl_t1,2))
            
            # check for close to close success
            if cl_t1<cl_t0:
                success_count_cl_cl+=1   
            # check for open to open success
            if op_t1<op_t0:
                success_count_op_op+=1
            # check for open to close success
            if op_t1<cl_t0:
                success_count_op_cl+=1
            # check for close to open success
            if cl_t1<op_t0:
                success_count_cl_op+=1
        
        ### 6.6 check for success based on bear signal
        elif est_signal == -1:
            
            # estimate pnl for each enter-exit option
            pnl_pct_cl_cl.append(round(-(cl_t0-cl_t1)*100/cl_t1,2))
            pnl_pct_op_op.append(round(-(op_t0-op_t1)*100/op_t1,2))
            pnl_pct_op_cl.append(round(-(cl_t0-op_t1)*100/op_t1,2))
            pnl_pct_cl_op.append(round(-(op_t0-cl_t1)*100/cl_t1,2))        
            
            # check for close to close success
            if cl_t1>cl_t0:
                success_count_cl_cl+=1        
            # check for open to open success
            if op_t1>op_t0:
                success_count_op_op+=1
            # check for open to close success
            if op_t1>cl_t0:
                success_count_op_cl+=1
            # check for close to open success
            if cl_t1>op_t0:
                success_count_cl_op+=1
        
        # check for no signal
        else:
            # do nothing
            success_count_cl_cl += 0 
        
    return count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op



def get_stats(est_df,count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op):
    
    # return null values in case everything is null    
    try:    
        # create statistics from pnl lists
        ### mean
        mean_cl_cl = np.mean(pnl_pct_cl_cl)
        mean_op_op = np.mean(pnl_pct_op_op)
        mean_op_cl = np.mean(pnl_pct_op_cl)
        mean_cl_op = np.mean(pnl_pct_cl_op)
        
        ### std dev
        std_cl_cl = np.std(pnl_pct_cl_cl)
        std_op_op = np.std(pnl_pct_op_op)
        std_op_cl = np.std(pnl_pct_op_cl)
        std_cl_op = np.std(pnl_pct_cl_op)
        
        ### sharpe ratio
        sr_cl_cl = mean_cl_cl/std_cl_cl
        sr_op_op = mean_op_op/std_op_op
        sr_op_cl = mean_op_cl/std_op_cl
        sr_cl_op = mean_cl_op/std_cl_op
        
        ### max profit (min loss)
        max_cl_cl = np.max(pnl_pct_cl_cl)
        max_op_op = np.max(pnl_pct_op_op)
        max_op_cl = np.max(pnl_pct_op_cl)
        max_cl_op = np.max(pnl_pct_cl_op)
        
        ### min profit (max loss)
        min_cl_cl = np.min(pnl_pct_cl_cl)
        min_op_op = np.min(pnl_pct_op_op)
        min_op_cl = np.min(pnl_pct_op_cl)
        min_cl_op = np.min(pnl_pct_cl_op)
        
        
        # choose the best entry_exit strategy
        if sr_cl_cl > max(sr_op_op,sr_cl_op,sr_op_cl):
            strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = "close-close",mean_cl_cl,std_cl_cl,sr_cl_cl,max_cl_cl,min_cl_cl,round(success_count_cl_cl*100/(len(est_df)-count_no_data-count_no_signal)),pnl_pct_cl_cl
        elif sr_op_op > max(sr_cl_cl,sr_cl_op,sr_op_cl):
            strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = "open-open",mean_op_op,std_op_op,sr_op_op,max_op_op,min_op_op,round(success_count_op_op*100/(len(est_df)-count_no_data-count_no_signal)),pnl_pct_op_op
        elif sr_op_cl > max(sr_cl_cl,sr_cl_op,sr_op_op):
            strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = "open-close",mean_op_cl,std_op_cl,sr_op_cl,max_op_cl,min_op_cl,round(success_count_op_cl*100/(len(est_df)-count_no_data-count_no_signal)),pnl_pct_op_cl
        elif sr_cl_op > max(sr_cl_cl,sr_op_op,sr_op_cl):
            strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = "close-open",mean_cl_op,std_cl_op,sr_cl_op,max_cl_op,min_cl_op,round(success_count_cl_op*100/(len(est_df)-count_no_data-count_no_signal)),pnl_pct_cl_op
    except:
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = "",np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
    return strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data