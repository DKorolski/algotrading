#!/usr/bin/env python
# coding: utf-8

import datetime  # get current time
import os
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from pandas_datareader import data  # downloading with pandas_datareader 
# list of data providers https://pandas-datareader.readthedocs.io/en/latest/remote_data.html


def download_from_file(src_path, start_date,end_date):
    #absolute to relative path change considered
    #start_date = '2020-01-12'
    #end_date = '2021-08-01'
    #src_path='C:\metastock_data\SPFB.RTS_190101_210731.csv'
    try:
        instrument_data = pd.read_csv(
            src_path, delimiter=',',
            parse_dates={'time': ['<DATE>', '<TIME>']},
            index_col=['time'],
            usecols=['<TICKER>', '<PER>','<DATE>', '<TIME>', 'open', 'High', 'Low', 'Close', 'volume'],
            names=['<TICKER>', '<PER>', '<DATE>', '<TIME>', 'open', 'High', 'Low', 'Close', 'volume'],
            header=0
            )
        instrument_data = instrument_data[start_date:end_date]
    except FileNotFoundError:
        print('Selected "' + src_path + '" not found')
    return instrument_data


def download_from_yahoo(ticker, start_date,end_date):
    try:
        instrument_data = pdr.DataReader(ticker, 'yahoo', start=start_date, end=end_date)
        instrument_data = instrument_data[start_date:end_date]
        return instrument_data
    except Exception:
        print('Selected "' + ticker + '" not found')
