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


def get_hist_data(stk):
    stock = yf.Ticker(stk)
    data = stock.history(period="900d")
    data = data.reset_index()
    return data

