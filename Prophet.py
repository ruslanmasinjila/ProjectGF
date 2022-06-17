#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from fbprophet import Prophet


# In[ ]:


with open('instruments.txt') as f:
    currency_pairs = [line.rstrip('\n') for line in f]


# In[ ]:


for i in currency_pairs:
  print(i)
  df = pd.read_csv(i,index_col=0)
  m = Prophet(interval_width=0.95)
  m.fit(df)
  future = m.make_future_dataframe(periods=1,freq="5 min")
  forecast = m.predict(future)
  toPlot = pd.DataFrame()
  toPlot["yhat"] = forecast["yhat"]
  toPlot["yhat_upper"] = forecast["yhat_upper"]
  toPlot["yhat_lower"] = forecast["yhat_lower"]
  toPlot["y"] = df["y"]
  toPlot.tail(1000).plot(title = i)

