#!/usr/bin/env python
# coding: utf-8

import datetime
import backtrader as bt
from datetime import datetime
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import quantstats
from data_loader import download_from_file
import backtrader.indicators as btind
from data_processor import *
#select strategy
from test_startegy_ema import *

# Instantiate Cerebro engine
cerebro = bt.Cerebro()

#setup instrument. timeframe for testing purposes --day
start_date = '2020-03-01'
end_date = '2021-08-09'
ticker = 'SBER.ME'

#download and process data
candles=get_candles(ticker, start_date,end_date)
df = bt.feeds.PandasData(dataname=candles)

#add processed data to engine
cerebro.adddata(df)

# Add strategy to Cerebro
cerebro.addstrategy(MAcrossover)

# Default position size
cerebro.broker.setcash(10000)
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

#choose analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')

if __name__ == '__main__':
    results=0
    startcash = 10000
    start_portfolio_value = cerebro.broker.getvalue()
    cerebro.broker.setcash(startcash)
    results = cerebro.run()
    strat = results[0]  
    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    portfolio_stats = strat.analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('DrawDown:', strat.analyzers.DrawDown.get_analysis())
    print('Final Balance: %.2f' % cerebro.broker.getvalue())
#print advanced testing results (not working)      
    quantstats.reports.html(returns, output='stats.html', title='TEST')
#plot shart
    cerebro.plot(style='candlestick',iplot=False)
    

        