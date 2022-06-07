#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##########################################################################################
# ProjectGF
# AUTHOR: RUSLAN MASINJILA
##########################################################################################
import MetaTrader5 as mt5
import pandas as pd
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
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15,M20,M30,H1,H2,H3,H4,H6,H8,H12,D1,W1,MN1]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15","M20","M30","H1","H2","H3","H4","H6","H8","H12","D1","W1","MN1"]

# TIMEFRAMES
mt5Timeframe   = [M1,M2,M3,M4,M5,M6,M10,M12,M15]
strTimeframe   = ["M1","M2","M3","M4","M5","M6","M10","M12","M15"]

numCandles     = 51
offset         = 1

RSIRainbowSignals   = []
RSIRainbowSignalsTF = []
##########################################################################################

# For testing
currency_pairs = ["EURUSD"]
mt5Timeframe   = [M1]
strTimeframe   = ["M1"]


# In[ ]:


def getSignals(rates_frame,strTimeframe):
    
    rates_frame["delta"] = rates_frame["close"].diff()
    
    averagePositiveGain50 = (rates_frame["delta"].tail(50)[rates_frame["delta"]>0].sum( ))/50
    averageNegativeLoss50 = ((-1)*rates_frame["delta"].tail(50)[rates_frame["delta"]<0].sum( ))/50
    RS50  = averagePositiveGain50/averageNegativeLoss50
    RSI50 = 100 - (100/(1+RS50))
    
    averagePositiveGain45 = (rates_frame["delta"].tail(45)[rates_frame["delta"]>0].sum( ))/45
    averageNegativeLoss45 = ((-1)*rates_frame["delta"].tail(45)[rates_frame["delta"]<0].sum( ))/45
    RS45  = averagePositiveGain45/averageNegativeLoss45
    RSI45 = 100 - (100/(1+RS45))
    
    averagePositiveGain40 = (rates_frame["delta"].tail(40)[rates_frame["delta"]>0].sum( ))/40
    averageNegativeLoss40 = ((-1)*rates_frame["delta"].tail(40)[rates_frame["delta"]<0].sum( ))/40
    RS40  = averagePositiveGain40/averageNegativeLoss40
    RSI40 = 100 - (100/(1+RS40))
    
    averagePositiveGain35 = (rates_frame["delta"].tail(35)[rates_frame["delta"]>0].sum( ))/35
    averageNegativeLoss35 = ((-1)*rates_frame["delta"].tail(35)[rates_frame["delta"]<0].sum( ))/35
    RS35  = averagePositiveGain35/averageNegativeLoss35
    RSI35 = 100 - (100/(1+RS35))
    
    averagePositiveGain30 = (rates_frame["delta"].tail(30)[rates_frame["delta"]>0].sum( ))/30
    averageNegativeLoss30 = ((-1)*rates_frame["delta"].tail(30)[rates_frame["delta"]<0].sum( ))/30
    RS30  = averagePositiveGain30/averageNegativeLoss30
    RSI30 = 100 - (100/(1+RS30))
    
    averagePositiveGain25 = (rates_frame["delta"].tail(25)[rates_frame["delta"]>0].sum( ))/25
    averageNegativeLoss25 = ((-1)*rates_frame["delta"].tail(25)[rates_frame["delta"]<0].sum( ))/25
    RS25  = averagePositiveGain25/averageNegativeLoss25
    RSI25 = 100 - (100/(1+RS25))
    
    averagePositiveGain20 = (rates_frame["delta"].tail(20)[rates_frame["delta"]>0].sum( ))/20
    averageNegativeLoss20 = ((-1)*rates_frame["delta"].tail(20)[rates_frame["delta"]<0].sum( ))/20
    RS20  = averagePositiveGain20/averageNegativeLoss20
    RSI20 = 100 - (100/(1+RS20))


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
        RainbowSignals =[]
        RainbowSignalsTF =[]
        for t in range(len(mt5Timeframe)):
            rates_frame = getRates(cp, mt5Timeframe[t], numCandles)
            getSignals(rates_frame,strTimeframe[t])
        if(all(x == RSIRainbowSignals[0] for x in RSIRainbowSignals)):
            if(len(RSIRainbowSignals)==len(mt5Timeframe)):
                display+=" ".join(RSIRainbowSignals)+"\n"
                display+=" ".join(RSIRainbowSignalsTF)+"\n"
                winsound.Beep(freq, duration)
                    
        display+="==============================\n"
    print(display)
    time.sleep(60)
    os.system('cls' if os.name == 'nt' else 'clear')

