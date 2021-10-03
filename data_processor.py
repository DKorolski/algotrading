#!/usr/bin/env python
# coding: utf-8

import datetime
from datetime import datetime
import pandas as pd
from pandas_datareader import data as pdr
import backtrader as bt
from data_loader import *


def get_candles(ticker, start_date,end_date):
    candles=download_from_yahoo(ticker, start_date,end_date)
    # dataset setup
    candles.columns=['high', 'low', 'open', 'close', 'volume', 'adj_close']
    return candles


        