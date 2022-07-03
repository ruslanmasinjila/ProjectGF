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
import math

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


numCandles     = 1000
offset         = 1
plotRange      = 500

##########################################################################################


# In[3]:


rates_frame =  mt5.copy_rates_from_pos("GBPUSD", M5, offset, numCandles)
rates_frame = pd.DataFrame(rates_frame)

rates_frame["median"] = (rates_frame["high"]+rates_frame["low"])/2
rates_frame["ema50"]  = ta.ema(rates_frame["median"],length=50)
rates_frame["ema45"]  = ta.ema(rates_frame["median"],length=45)
rates_frame["ema40"]  = ta.ema(rates_frame["median"],length=40)
rates_frame["ema35"]  = ta.ema(rates_frame["median"],length=35)
rates_frame["ema30"]  = ta.ema(rates_frame["median"],length=30)
rates_frame["ema25"]  = ta.ema(rates_frame["median"],length=25)
rates_frame["ema20"]  = ta.ema(rates_frame["median"],length=20)


rates_frame["ema50_velocity"] = rates_frame["ema50"].diff()
rates_frame["ema45_velocity"] = rates_frame["ema45"].diff()
rates_frame["ema40_velocity"] = rates_frame["ema40"].diff()
rates_frame["ema35_velocity"] = rates_frame["ema35"].diff()
rates_frame["ema30_velocity"] = rates_frame["ema30"].diff()
rates_frame["ema25_velocity"] = rates_frame["ema25"].diff()
rates_frame["ema20_velocity"] = rates_frame["ema20"].diff()

rates_frame["ema_velocity_sum"] = rates_frame["ema50_velocity"]+rates_frame["ema45_velocity"]+rates_frame["ema40_velocity"]+                                    rates_frame["ema35_velocity"]+rates_frame["ema30_velocity"]+rates_frame["ema25_velocity"]+                                        rates_frame["ema20_velocity"]
                            

rates_frame["ema50_acceleration"] = rates_frame["ema50_velocity"].diff()
rates_frame["ema45_acceleration"] = rates_frame["ema45_velocity"].diff()
rates_frame["ema40_acceleration"] = rates_frame["ema40_velocity"].diff()
rates_frame["ema35_acceleration"] = rates_frame["ema35_velocity"].diff()
rates_frame["ema30_acceleration"] = rates_frame["ema30_velocity"].diff()
rates_frame["ema25_acceleration"] = rates_frame["ema25_velocity"].diff()
rates_frame["ema20_acceleration"] = rates_frame["ema20_velocity"].diff()

rates_frame["ema_acceleration_sum"] = rates_frame["ema50_acceleration"]+rates_frame["ema45_acceleration"]+rates_frame["ema40_acceleration"]+                                        rates_frame["ema35_acceleration"]+rates_frame["ema30_acceleration"]+rates_frame["ema25_acceleration"]+                                            rates_frame["ema20_acceleration"]


rates_frame["resultant"] = (rates_frame["ema_velocity_sum"]**2 + rates_frame["ema_acceleration_sum"]**2)**(1/2)


# In[4]:


rates_frame["ema_velocity_sum"].tail(plotRange).plot(style="*-")


# In[5]:


rates_frame[['ema50_velocity', 'ema45_velocity','ema40_velocity','ema35_velocity','ema30_velocity','ema25_velocity','ema20_velocity']].tail(plotRange).plot()


# In[6]:


rates_frame[['ema50', 'ema45','ema40','ema35','ema30','ema25','ema20']].tail(plotRange).plot()


# In[7]:


rates_frame["close"].tail(plotRange).plot(style="*-")

