# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 20:00:45 2021

@author: anshu
"""
# import packages
import pandas as pd
import numpy as np

# read stock list file
stock_df = pd.read_csv('../output/stock_list_2.csv')
res_list = []

# get pattern data for the stocks
for itr in range(len(stock_df)):
    stock = stock_df.iloc[itr]['name']
    try:
        df = pd.read_csv('../output/'+stock+'.csv')
        df = df.T
        df.columns = ['est_val','est_cnt','wall_st','act_val','yoy_growth']
        df = df.iloc[1:]
        
        count = 0
        count_valid=0
        pct_diff_list = []
        for i in range(len(df)):
            est = (df.iloc[i]['est_val'])
            wst = (df.iloc[i]['wall_st'])
            act = (df.iloc[i]['act_val'])
            
            if (est=='-') | (wst=='-') | (act=='-'):
                continue
            else:
                count_valid+=1
                est,wst,act = float(est),float(wst),float(act)            
                
                if abs(est-act)<abs(wst-act):
                    count=count+1
                    
                # calculate percentage diff between estimize and wall street estimates
                tmp_pct_diff = round(abs(est-wst)*100/abs(wst))
                pct_diff_list.append(tmp_pct_diff)
                
        hit_pct = round(count*100/len(df))
        last_4_cnt_list = [int(x) for x in df.iloc[-4:]['est_cnt'].fillna(0).values]
        avg_usr_cnt = np.mean(last_4_cnt_list)
        
        pct_diff = np.mean(pct_diff_list)
        
        res_list.append({'name':stock,'earn_date':stock_df.iloc[itr]['earn_date'],'earn_time':stock_df.iloc[itr]['earn_time'],'earn_day':stock_df.iloc[itr]['earn_day'],'link':stock_df.iloc[itr]['link'],'hit_rate':hit_pct,'valid_count':count_valid,'4_part_cnt':avg_usr_cnt,'pct_diff':pct_diff})
        
      
    except:
        continue

# save the file    
res_df = pd.DataFrame(res_list)
# print(res_df)
res_df.to_csv('../output/stock_hit_rate_2.csv')