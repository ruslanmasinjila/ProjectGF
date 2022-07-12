#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


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


# In[ ]:


def getSignals(rates_frame,strTimeframe):
    
    rates_frame["median"] = (rates_frame["high"]+rates_frame["low"])/2
    rates_frame["ema50"] = ta.ema(rates_frame["median"],length=50)
    rates_frame["ema45"] = ta.ema(rates_frame["median"],length=45)
    rates_frame["ema40"] = ta.ema(rates_frame["median"],length=40)
    rates_frame["ema35"] = ta.ema(rates_frame["median"],length=35)
    rates_frame["ema30"] = ta.ema(rates_frame["median"],length=30)
    rates_frame["ema25"] = ta.ema(rates_frame["median"],length=25)
    rates_frame["ema20"] = ta.ema(rates_frame["median"],length=20)
    
    
    leftOpen          = rates_frame.iloc[-3].open
    leftClose         = rates_frame.iloc[-3].close
    leftEMA50         = rates_frame.iloc[-3].ema50
    leftEMA45         = rates_frame.iloc[-3].ema45
    leftEMA40         = rates_frame.iloc[-3].ema40
    leftEMA35         = rates_frame.iloc[-3].ema35
    leftEMA30         = rates_frame.iloc[-3].ema30
    leftEMA25         = rates_frame.iloc[-3].ema25
    leftEMA20         = rates_frame.iloc[-3].ema20
    
    
    middleOpen          = rates_frame.iloc[-2].open
    middleClose         = rates_frame.iloc[-2].close
    middleEMA50         = rates_frame.iloc[-2].ema50
    middleEMA45         = rates_frame.iloc[-2].ema45
    middleEMA40         = rates_frame.iloc[-2].ema40
    middleEMA35         = rates_frame.iloc[-2].ema35
    middleEMA30         = rates_frame.iloc[-2].ema30
    middleEMA25         = rates_frame.iloc[-2].ema25
    middleEMA20         = rates_frame.iloc[-2].ema20
    
    rightOpen           = rates_frame.iloc[-1].open
    rightClose          = rates_frame.iloc[-1].close
    
    
    if(leftEMA50<leftEMA45 and
       leftEMA45<leftEMA40 and
       leftEMA40<leftEMA35 and
       leftEMA35<leftEMA30 and
       leftEMA30<leftEMA25 and
       leftEMA25<leftEMA20):
        if(middleEMA50<middleEMA45 and
           middleEMA45<middleEMA40 and
           middleEMA40<middleEMA35 and
           middleEMA35<middleEMA30 and
           middleEMA30<middleEMA25 and
           middleEMA25<middleEMA20):
            if(leftOpen<leftEMA50 and leftClose>leftEMA50 and leftClose<leftEMA20):
                if(middleOpen>middleEMA50 and middleOpen<middleEMA20 and middleClose>middleEMA20):
                    if(rightClose>rightOpen):
                        EMARainbowSignals.append("[BUY | " +strTimeframe+"]")
                    
    if(leftEMA50>leftEMA45 and
       leftEMA45>leftEMA40 and
       leftEMA40>leftEMA35 and
       leftEMA35>leftEMA30 and
       leftEMA30>leftEMA25 and
       leftEMA25>leftEMA20):
        if(middleEMA50>middleEMA45 and
           middleEMA45>middleEMA40 and
           middleEMA40>middleEMA35 and
           middleEMA35>middleEMA30 and
           middleEMA30>middleEMA25 and
           middleEMA25>middleEMA20):
            if(leftOpen>leftEMA50 and leftClose<leftEMA50 and leftClose>leftEMA20):
                if(middleOpen<middleEMA50 and middleOpen>middleEMA20 and middleClose<middleEMA20):
                    if(rightClose<rightOpen):
                        EMARainbowSignals.append("[SELL | " +strTimeframe+"]")

##########################################################################################


# In[ ]:


# Gets the most recent <numCandles> prices for a specified <currency_pair> and <mt5Timeframe>
# Excludes the bar that has not finished forming <i.e offset = 1>
def getRates(currency_pair, mt5Timeframe, numCandles):
    rates_frame =  mt5.copy_rates_from_pos(currency_pair, mt5Timeframe, offset, numCandles)
    rates_frame = pd.DataFrame(rates_frame)
    return rates_frame

##########################################################################################


# In[ ]:


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

