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



# 1. initialise the dataframe to get the final results and get the list of stocks
final_df = pd.DataFrame()
hit_df = pd.read_csv('../output/stock_hit_rate.csv')
stock_list = list(hit_df['name'])



for stk in stock_list:
    # 2. get the stock object
    stock = yf.Ticker(stk)
    
    
    
    # 3. get the historical data and analytics from estimize
    data = stock.history(period="600d")
    data = data.reset_index()
    
    
    
    # 4. get the earning dates
    
    ### 4.1 read data from yahoo_fin 
    earning_hist = si.get_earnings_history(stk)
    earning_hist_df = pd.DataFrame(earning_hist)
    # print(earning_hist_df)
    # earning_hist_df.to_csv('../output/earning_data.csv')
    
    ### 4.2 drop duplicate dates
    earning_hist_df['date'] = earning_hist_df.startdatetime.str[:10]
    earning_hist_df = earning_hist_df.drop_duplicates(subset=['date'])
    
    ### 4.3 drop the future eps dates
    earning_hist_df = earning_hist_df.dropna(subset=['epsactual'])
    # print(earning_hist_df)
    # earning_hist_df.to_csv('../output/earning_data_upd.csv')
    dates = [x[:10] for x in list(earning_hist_df.iloc[:8]['date'])]
    # print(dates)
    
    
    
    # 5. initialise variables and process estimize dataset
    
    ### 5.1 read and process stock data from estimize
    est_df = pd.read_csv('../output/'+stk+'.csv').T
    est_df = est_df.iloc[1:]
    est_df.columns = ['est_val','est_cnt','wl_st','act','yoy']
    est_df['date'] = dates
    # print(est_df)
    
    ### 5.2 initialise success count for various enter-exit option
    success_count_cl_cl = 0
    success_count_op_cl = 0
    success_count_cl_op = 0
    success_count_op_op = 0
    
    ### 5.3 initialise pnl pct list for various enter-exit option
    pnl_pct_cl_cl = []
    pnl_pct_op_cl = []
    pnl_pct_cl_op = []
    pnl_pct_op_op = []
    
    ### 5.4 initialise the count for no signal
    # to counter cases where the estimize consensus is missing
    count_no_signal = 0
    
    
    
    # 6. iterate over each quarterly earnings
    for i in range(len(est_df)):
        ### 6.1 get historical data for earning day and 1 day prior 
        dt = est_df.iloc[i]['date']
        # print("date: ",dt)
        idx = data[data['Date']==dt].index[0]
        tmp = data.loc[data.index.isin([idx-1,idx])]
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
    
    
    
    # 7. create statistics from pnl lists
    
    ### 7.1 mean
    mean_cl_cl = np.mean(pnl_pct_cl_cl)
    mean_op_op = np.mean(pnl_pct_op_op)
    mean_op_cl = np.mean(pnl_pct_op_cl)
    mean_cl_op = np.mean(pnl_pct_cl_op)
    
    ### 7.2 std dev
    std_cl_cl = np.std(pnl_pct_cl_cl)
    std_op_op = np.std(pnl_pct_op_op)
    std_op_cl = np.std(pnl_pct_op_cl)
    std_cl_op = np.std(pnl_pct_cl_op)
    
    ### 7.3 sharpe ratio
    sr_cl_cl = mean_cl_cl/std_cl_cl
    sr_op_op = mean_op_op/std_op_op
    sr_op_cl = mean_op_cl/std_op_cl
    sr_cl_op = mean_cl_op/std_cl_op
    
    ### 7.4 max profit (min loss)
    max_cl_cl = np.max(pnl_pct_cl_cl)
    max_op_op = np.max(pnl_pct_op_op)
    max_op_cl = np.max(pnl_pct_op_cl)
    max_cl_op = np.max(pnl_pct_cl_op)
    
    ### 7.5 min profit (max loss)
    min_cl_cl = np.min(pnl_pct_cl_cl)
    min_op_op = np.min(pnl_pct_op_op)
    min_op_cl = np.min(pnl_pct_op_cl)
    min_cl_op = np.min(pnl_pct_cl_op)
    
    
    
    # 8. choose the best entry_exit strategy
    if sr_cl_cl > max(sr_op_op,sr_cl_op,sr_op_cl):
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt = "close-close",mean_cl_cl,std_cl_cl,sr_cl_cl,max_cl_cl,min_cl_cl,round(success_count_cl_cl*100/len(est_df))
    elif sr_op_op > max(sr_cl_cl,sr_cl_op,sr_op_cl):
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt = "open-open",mean_op_op,std_op_op,sr_op_op,max_op_op,min_op_op,round(success_count_op_op*100/len(est_df))
    elif sr_op_cl > max(sr_cl_cl,sr_cl_op,sr_op_op):
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt = "open-close",mean_op_cl,std_op_cl,sr_op_cl,max_op_cl,min_op_cl,round(success_count_op_cl*100/len(est_df))
    elif sr_cl_op > max(sr_cl_cl,sr_op_op,sr_op_cl):
        strat_opt,mean_opt,std_opt,sr_opt,max_opt,min_opt,success_opt = "close-open",mean_cl_op,std_cl_op,sr_cl_op,max_cl_op,min_cl_op,round(success_count_cl_op*100/len(est_df))
    
    
    
    # 9. get the date of next earning
    earn_date = si.get_next_earnings_date(stk)
    today = earn_date
    one_day_prior = today - BDay(1)
    three_day_prior = today - BDay(3)
    five_day_prior = today - BDay(5)
    
    
    
    # 10. save the entries for the stock in the dataframe
    
    ### 10.1 read the relevant data points from estimize based stock_hit_rate file
    tmp_df = hit_df.loc[hit_df['name']==stk]
    
    ### 10.2 save the data in res_df
    res_list = []
    res_list.append({
                     'name':stk, 'earn_dt':earn_date, '1_prior':one_day_prior, '3_prior':three_day_prior, 
                     '5_prior':five_day_prior, 'est_hit_rate':tmp_df['hit_rate'].values[0], 'valid_data_pct':round((tmp_df['valid_count'].values[0])*100/len(est_df)),
                     'last_4_est_cnt':tmp_df['4_part_cnt'].values[0],'est_wl_pct_diff':tmp_df['pcct_diff'].values[0], 'opt_str':strat_opt, 'opt_sr':sr_opt,
                     'opt_mean':mean_opt, 'opt_std':std_opt, 'opt_max':max_opt, 'opt_min':min_opt, 'mkt_hit_rate':success_opt, 'net_hit_rate':round(tmp_df['hit_rate'].values[0]*success_opt/100),
                     'link':tmp_df['link'].values[0]
                     })
    res_df = pd.DataFrame(res_list)
    final_df = pd.concat([final_df,res_df],ignore_index=True)
    
    
    
# 11. Save the final dataframe    
final_df.to_csv('../output/final_output.csv')