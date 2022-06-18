#!/usr/bin/env python
# coding: utf-8

# In[13]:


##########################################################################################
# DataFetcher
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np
import time
import os

# NUMBER OF COLUMNS TO BE DISPLAYED
pd.set_option('display.max_columns', 500)

# MAXIMUM TABLE WIDTH TO DISPLAY
pd.set_option('display.width', 1500)      
 
# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print("initialize() FAILED, ERROR CODE =",mt5.last_error())
    quit()


# In[14]:


# MT5 TIMEFRAME
MN1  = mt5.TIMEFRAME_MN1
W1  = mt5.TIMEFRAME_W1
D1  = mt5.TIMEFRAME_D1
H12 = mt5.TIMEFRAME_H12
H8  = mt5.TIMEFRAME_H8
H6  = mt5.TIMEFRAME_H6
H4  = mt5.TIMEFRAME_H4
H3  = mt5.TIMEFRAME_H3
H2  = mt5.TIMEFRAME_H2
H1  = mt5.TIMEFRAME_H1
M30 = mt5.TIMEFRAME_M30
M20 = mt5.TIMEFRAME_M20
M15 = mt5.TIMEFRAME_M15
M12 = mt5.TIMEFRAME_M12
M10 = mt5.TIMEFRAME_M10
M6  = mt5.TIMEFRAME_M6
M5  = mt5.TIMEFRAME_M5
M4  = mt5.TIMEFRAME_M4
M3  = mt5.TIMEFRAME_M3
M2  = mt5.TIMEFRAME_M2
M1  = mt5.TIMEFRAME_M1

currency_pairs = None
with open('instruments.txt') as f:
    currency_pairs = [line.rstrip('\n') for line in f]


# TIMEFRAMES
# mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
# strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1"]

mt5Timeframe   =   M5
strTimeframe   =  "M5"

numCandles     = 10000
offset         = 1
##########################################################################################


# In[15]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
# Excludes the bar that has not finished forming <i.e offset = 1>
# Saves the rates in .csv files
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame["rsi"] = ta.rsi(rates_frame["close"],length=100)
    rates_frame=rates_frame.dropna().reset_index(drop=True)
    rates_frame.drop(["open","high","low","close","tick_volume","spread","real_volume"],axis = 1, inplace=True)
    rates_frame.rename(columns={"time": "ds", "rsi": "y"},inplace=True)
    rates_frame.to_csv("rates/"+cp+".csv")

##########################################################################################


# In[16]:


for cp in currency_pairs:
    getRates(cp, mt5Timeframe, numCandles)

