#!/usr/bin/env python
# coding: utf-8

# In[1]:


##########################################################################################
# ProjectGF
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np
import time
import os

import winsound
duration = 100
freq     = 1000

# NUMBER OF COLUMNS TO BE DISPLAYED
pd.set_option('display.max_columns', 500)

# MAXIMUM TABLE WIDTH TO DISPLAY
pd.set_option('display.width', 1500)      
 
# ESTABLISH CONNECTION TO MT5 TERMINAL
if not mt5.initialize():
    print("initialize() FAILED, ERROR CODE =",mt5.last_error())
    quit()


# In[2]:


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
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1"]

numCandles     = 1000
offset         = 1

EMARainbowSignals   = []
##########################################################################################


# In[3]:


def getSignals(rates_frame,strTimeframe):
    
    rates_frame["median"] = (rates_frame["high"]+rates_frame["low"])/2
    rates_frame["ema50"] = ta.ema(rates_frame["median"],length=50)
    rates_frame["ema45"] = ta.ema(rates_frame["median"],length=45)
    rates_frame["ema40"] = ta.ema(rates_frame["median"],length=40)
    rates_frame["ema35"] = ta.ema(rates_frame["median"],length=35)
    rates_frame["ema30"] = ta.ema(rates_frame["median"],length=30)
    rates_frame["ema25"] = ta.ema(rates_frame["median"],length=25)
    rates_frame["ema20"] = ta.ema(rates_frame["median"],length=20)
    
    
    previousOpen          = rates_frame.iloc[-2].open
    previousClose         = rates_frame.iloc[-2].close
    previousEMA50         = rates_frame.iloc[-2].ema50
    previousEMA45         = rates_frame.iloc[-2].ema45
    previousEMA40         = rates_frame.iloc[-2].ema40
    previousEMA35         = rates_frame.iloc[-2].ema35
    previousEMA30         = rates_frame.iloc[-2].ema30
    previousEMA25         = rates_frame.iloc[-2].ema25
    previousEMA20         = rates_frame.iloc[-2].ema20
    
    
    currentOpen          = rates_frame.iloc[-1].open
    currentClose         = rates_frame.iloc[-1].close
    currentEMA50         = rates_frame.iloc[-1].ema50
    currentEMA45         = rates_frame.iloc[-1].ema45
    currentEMA40         = rates_frame.iloc[-1].ema40
    currentEMA35         = rates_frame.iloc[-1].ema35
    currentEMA30         = rates_frame.iloc[-1].ema30
    currentEMA25         = rates_frame.iloc[-1].ema25
    currentEMA20         = rates_frame.iloc[-1].ema20
    
    
    if(previousEMA50<previousEMA45 and
       previousEMA45<previousEMA40 and
       previousEMA40<previousEMA35 and
       previousEMA35<previousEMA30 and
       previousEMA30<previousEMA25 and
       previousEMA25<previousEMA20):
        if(currentEMA50<currentEMA45 and
           currentEMA45<currentEMA40 and
           currentEMA40<currentEMA35 and
           currentEMA35<currentEMA30 and
           currentEMA30<currentEMA25 and
           currentEMA25<currentEMA20):
            if(previousOpen<previousEMA50 and previousClose>previousEMA50 and previousClose<previousEMA20):
                if(currentOpen>currentEMA50 and currentOpen<currentEMA20 and currentClose>currentEMA20):
                    EMARainbowSignals.append("[BUY | " +strTimeframe+"]")
                    
    if(previousEMA50>previousEMA45 and
       previousEMA45>previousEMA40 and
       previousEMA40>previousEMA35 and
       previousEMA35>previousEMA30 and
       previousEMA30>previousEMA25 and
       previousEMA25>previousEMA20):
        if(currentEMA50>currentEMA45 and
           currentEMA45>currentEMA40 and
           currentEMA40>currentEMA35 and
           currentEMA35>currentEMA30 and
           currentEMA30>currentEMA25 and
           currentEMA25>currentEMA20):
            if(previousOpen>previousEMA50 and previousClose<previousEMA50 and previousClose>previousEMA20):
                if(currentOpen<currentEMA50 and currentOpen>currentEMA20 and currentClose<currentEMA20):
                    EMARainbowSignals.append("[SELL | " +strTimeframe+"]")

##########################################################################################


# In[4]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
# Excludes the bar that has not finished forming <i.e offset = 1>
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################


# In[5]:


banner = ""
banner+="##############################\n"
banner+="           SIGNALS            \n"
banner+="##############################\n"
while(True):
    
    display = banner
    for cp in currency_pairs:
        display+="["+cp+"]"+"\n"
        EMARainbowSignals =[]
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
        if(len(EMARainbowSignals)>0):
            display+=" ".join(EMARainbowSignals)+"\n"
            winsound.Beep(freq, duration)

        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')

