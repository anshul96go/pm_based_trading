# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 20:55:36 2022

@author: anshu
"""

import pandas as pd
import datetime

df = pd.read_csv('../output/stock_list_2.csv')
print(df['earn_date'].unique())

print("--------------------------------------")

for i in range(len(df)):
    dt = df.iloc[i]['earn_date']
    try:
        x = datetime.date(1899,12,30) + datetime.timedelta(days=float(dt))
        df.loc[i,'earn_date'] = x.strftime('%m/%d/%Y')
    except:
        df.loc[i,'earn_date'] = pd.to_datetime(dt)
print(df['earn_date'].unique())

df['earn_date'] = df['earn_date'].astype(str).str[:10]

df.to_csv('../output/stock_list_2.csv')