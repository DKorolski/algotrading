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
from data_processor import get_candles
#select strategy
from test_startegy_ema import MAcrossover

# Instantiate Cerebro engine for optimizing purposes
# Comment  line 23 (logging) in stategy class test_startegy_ema when running optimization
cerebro = bt.Cerebro(optreturn=False)

#setup instrument. timeframe for testing purposes --day
start_date = '2020-11-01'
end_date = '2021-08-09'
ticker = 'SBER.ME'

#download and process data
candles=get_candles(ticker, start_date,end_date)
df = bt.feeds.PandasData(dataname=candles)

#add processed data to engine
cerebro.adddata(df)

# Add strategy to Cerebro within arguments
cerebro.optstrategy(MAcrossover, pfast=range(5, 20),pslow=range(7, 60))  

# Default position size
cerebro.broker.setcash(10000)
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

#choose analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

if __name__ == '__main__':
    results=0
    startcash = 10000
    start_portfolio_value = cerebro.broker.getvalue()
    cerebro.broker.setcash(startcash)
    optimized_runs=0
    optimized_runs = cerebro.run()
    if optimized_runs !=0:
        final_results_list = []
        for run in optimized_runs:
            for strategy in run:
                PnL = round(strategy.broker.get_value() - 10000,2)
                sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
                tradean= strategy.analyzers.trades.get_analysis()
                try:
                    final_results_list.append([strategy.params.pfast, 
                    strategy.params.pslow, PnL, sharpe['sharperatio'],tradean.total['total'],tradean.won['total'],tradean.lost['total'],tradean.long['total']]) 
                    sort_by_sharpe = sorted(final_results_list, key=lambda x: x[7], 
                                reverse=True)
                except:
                    print('not enough data...')
        for line in sort_by_sharpe[:5]:
            
            print(line)
    

        