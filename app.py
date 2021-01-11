# used libs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import datetime
from dateutil.relativedelta import relativedelta
import time
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


# Start execute
start_time = time.time()

# /////////////////////////////////////////////////////////////////////////////

# Utils

# /////////////////////////////////////////////////////////////////////////////


def get_data(tickers,start,end):
  df = yf.download(
          tickers = tickers,
          # period = "ytd",
          start = start,
          end = end,
          interval = "1d",
          # group_by = 'ticker',
          auto_adjust = True,
          prepost = True,
          threads = True,
          proxy = None
      )
  return df

def get_ticker(data,target,tickers):
  if len(tickers) > 1:
    df = data[target].copy()
  else:
    df = data[[target]].copy()
    df.columns = tickers
  return df

def scale_data(scale, data):
  df = data.copy()
  columns = df.columns
  if scale == 'Normalized':
    scaler = RobustScaler()
    df[columns] = scaler.fit_transform(df)
  return df

def plot_data(data, target,tickers):
  fig = plt.figure(figsize=(7,4))
  columns = list(data.columns)
  for column in columns:
    plt.plot(data.index, data[column], label=column)

  if len(tickers) > 1:
    plot_title = 'Compared {} Tickers'.format(len(tickers))
  else:
    plot_title = '{}'.format(tickers[0])

  plt.xticks(rotation=45)
  plt.legend()
  plt.title(plot_title, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('{}'.format(target), fontweight='bold')  
  return st.pyplot(fig)

# /////////////////////////////////////////////////////////////////////////////

# Side Bar: select parameters

# /////////////////////////////////////////////////////////////////////////////


# side bar: 1st component
## get tickers

st.sidebar.header('User Input Features')

input_default = 'AAPL, TSLA'
input_tickers = st.sidebar.text_input('Select tickers', input_default)

target_list = ['Close', 'High', 'Low', 'Open', 'Volume']
target = st.sidebar.selectbox('Choose Metric', target_list)

if len(input_tickers) > 1:
  ticker_list = [x.strip() for x in input_tickers.split(',')]
elif len(input_tickers) == 0:
  ticker_list = ['AAPL']

# side bar: 2nd component
## get date

start_dt = st.sidebar.date_input(
    'Start',
    datetime.datetime.today() + relativedelta(years=-3)
)
end_dt = st.sidebar.date_input(
    'End',
    datetime.datetime.today()
)

# side bar: 3rd component
scale = st.sidebar.radio('Data:', ['Raw','Normalized'])

# get data for visualization
data = get_data(ticker_list, start_dt,  end_dt)
df = get_ticker(data, target, ticker_list)
plot_df = scale_data(scale, df)

# /////////////////////////////////////////////////////////////////////////////

# Main App

# /////////////////////////////////////////////////////////////////////////////


# App Title

if len(ticker_list) > 1:
  app_title = 'Stock Comparing'
  msg = 'compares stocks by using their **{}** prices.'.format(target)
else:
  app_title = '{}: {}'.format(ticker_list[0], target)
  msg = 'displays a stock **{}** prices.'.format(target)

st.title(app_title)

st.markdown("""
This app {}
* **Data source:** yahoo finance.
""".format(msg))

plot_data(plot_df,target,ticker_list)
end_time = time.time()
elapsed = end_time-start_time
st.write('executed in {:.4f}s'.format(elapsed))