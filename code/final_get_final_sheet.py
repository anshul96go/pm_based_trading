# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 14:24:29 2021

@author: anshu
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 22:53:35 2021

@author: anshu
"""

# 0. import package
import yfinance as yf
import pandas as pd
import numpy as np
import yahoo_fin.stock_info as si
import datetime
from pandas.tseries.offsets import BDay
from helper_get_final_sheet import *
from helper_2 import *


# 1. initialise the dataframe to get the final results and get the list of stocks
try:
    final_df = pd.read_csv('../output/final_output.csv')
except:
    final_df = pd.DataFrame()
hit_df = pd.read_csv('../output/stock_hit_rate.csv')
stock_list = list(hit_df['name'])
stock_list.remove('CWEN')

counter=0
issue_stocks = []
for stk in stock_list:
    if stk in list(final_df['name']):
        print("stk in final output: ",stk)
        continue
    else:    
        counter+=1
        print("stk, counter ",stk,counter)
        print("len issue stocks: ",len(issue_stocks))
        
        # get the historical data
        data = pd.read_csv('../hist_data/' + stk + '_2000d.csv')
        
        # get the past earning dates
        dates = get_past_earning_dates(stk)
        
        # if there is any issue with past earning dates, ignore the stock
        if len(dates)!=8:
            print("date issue: ",stk)
            issue_stocks.append(stk)
            continue
        
        # get estimize data
        # this try except thing also eliminates stock which has missing values in their estimize table
        try:
            est_df = get_estimize_data(stk,dates)
        except:
            print("Code Error: estimize data is not available for ",stk)
            issue_stocks.append(stk)
            continue
            
        
        # get stats for the stock
        count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op=get_qtr_earn_stats_trial(est_df,data)
        # print("count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op \n", count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op)
        
        # get the optimal strategy for the stock
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data = get_stats(est_df,count_no_signal,count_no_data,success_count_cl_cl,success_count_op_cl,success_count_cl_op,success_count_op_op,pnl_pct_cl_cl,pnl_pct_op_cl,pnl_pct_cl_op,pnl_pct_op_op)
        # print("strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data \n",strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt,success_data)
        
        # get the next earning dates
        try:
            earn_date = si.get_next_earnings_date(stk)
            today = earn_date
            one_day_prior = today - BDay(1)
            three_day_prior = today - BDay(3)
            five_day_prior = today - BDay(5)
        except:
            earn_date = np.nan
            one_day_prior = np.nan
            three_day_prior = np.nan
            five_day_prior = np.nan
            
        
        # save the entries for the stock in the dataframe
        ### read the relevant data points from estimize based stock_hit_rate file
        tmp_df = hit_df.loc[hit_df['name']==stk]
        
        ## save the data in res_df
        res_list = []
        res_list.append({
                          'name':stk, 'earn_dt':earn_date, '1_prior':one_day_prior, '3_prior':three_day_prior, 
                          '5_prior':five_day_prior, 'est_hit_rate':tmp_df['hit_rate'].values[0], 'valid_data_pct':round((tmp_df['valid_count'].values[0])*100/len(est_df)),
                          'last_4_est_cnt':tmp_df['4_part_cnt'].values[0],'est_wl_pct_diff':tmp_df['pcct_diff'].values[0], 'opt_str':strat_opt, 'opt_sr':sr_opt,
                          'opt_mean':mean_opt, 'opt_std':std_opt, 'opt_max':max_opt, 'opt_min':min_opt, 'mkt_hit_rate':success_opt, 'net_hit_rate':round(tmp_df['hit_rate'].values[0]*success_opt/100),
                          'valid_market_data':round((len(est_df) - count_no_data)*100/len(est_df)),
                          'valid_est_signal':round((len(est_df) - count_no_signal)*100/len(est_df)),'link':tmp_df['link'].values[0],
                          'past_pnl_data':success_data          
                          })
        res_df = pd.DataFrame(res_list)
        
        final_df = pd.concat([final_df,res_df],ignore_index=True)
    
    
    
        # save the final dataframe    
        final_df.to_csv('../output/final_output.csv')        
    