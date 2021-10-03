import backtrader as bt
from pinescript import line2arr, barssince, valuewhen, na, nz
import numpy as np
import datetime
from datetime import time, timedelta


class MAcrossover(bt.Strategy): 
    '''
    This strategy is loosely based on EMA crossover. The logic:
      - Enter the market if:
        - The fast ema indicator crosses up the slow-one 
        - The fast ema indicator crosses down the slow-one 
     - If in the market:
       - Check for the crossover
    '''

    # Moving average parameters
    params = (('pfast',5),('pslow',10),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
    #    print(f'{dt.isoformat()} {txt}') # Comment this line when running optimization

    def __init__(self):
        self.dataclose = self.datas[0].close
        
        
		# Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate moving averages
        self.slow_sma = bt.indicators.ExponentialMovingAverage(self.datas[0], 
                        period=self.params.pslow)
        self.fast_sma = bt.indicators.ExponentialMovingAverage(self.datas[0], 
                        period=self.params.pfast)
        self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades
                
            #If the 20 SMA is above the 50 SMA
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(size=20)
            #Otherwise if the 20 SMA is below the 50 SMA   
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=20)
        else:
            # We are already in the market, look for a signal to CLOSE trades
   #         if len(self) >= (self.bar_executed + 1):
            if self.crossover!=0: #or len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close(size=20)