# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

class MyIndicator(bt.Indicator):
    lines =('up','down','signal')
    def __init__(self):
        #self.addminperiod(4)
        self.plotinfo.plotmaster = self.data
        self.highest_value = 77
        self.lowest_value = 99999
        self.trend = 0
        
        self.space = 1
        print('Myindicator initialized')
    def prenext(self):
        print("Myindicator PRENEXT")
    def nextstart(self):
        self.highest_value = max(self.highest_value, self.data.high[0])
        self.down[0] = self.highest_value - self.space
        
        self.lowest_value = min(self.lowest_value, self.data.low[0])
        self.up[0] = self.lowest_value + self.space
        if self.data.close[0] > self.data.open[0]:
            self.signal[0] = 1
        else: self.signal[0] = -1
        #self.signal[0] = 0    
    def next(self):
        if self.signal[-1] == -1:
            if self.data.high[0] > self.up[-1]:
                self.signal[0] = 1
                self.highest_value = 0
                self.highest_value = max(self.highest_value, self.data.high[0])
                self.down[0] = self.highest_value - 1
            else:
                self.lowest_value = min(self.lowest_value, self.data.low[0])
                self.up[0] = self.lowest_value + 1
        
        if self.signal[-1] == 1:
            if self.data.low[0] < self.down[-1]:
                self.signal[0] = -1
                self.lowest_value = 99999
                self.lowest_value = min(self.lowest_value, self.data.low[0])
                self.up[0] = self.lowest_value + 1
            else:
                self.lowest_value = min(self.lowest_value, self.data.low[0])
                self.up[0] = self.lowest_value + 1
            
        print('INDICATORmmm', self.highest_value)
        if self.trend == 1 :
            if self.data.low[0] >= self.down[-1]:
                self.highest_value = max(self.highest_value, self.data.high[0])
                self.down[0] = self.highest_value  - 2
            if self.data.low[0] < self.down[-1]:
                self.lowest_value = 99999
                self.lowest_value = min(self.lowest_value, self.data.low[0])
                
                self.up[0] = self.lowest_value + 2
                self.trend = -1
            
        if self.trend == -1 :
            #self.up[0] = self.up[-1]
            if self.data.high[0] <= self.up[-1]:
                self.lowest_value = min(self.lowest_value, self.data.low[0])
                self.up[0] = self.lowest_value + 2
            if self.data.high[0] > self.up[-1]:
                self.highest_value = 0
                self.highest_value = max(self.highest_value, self.data.high[0])
                self.down[0] = self.highest_value - 2
               
                self.trend = 1

        
        if self.trend == 0 and self.signal == 0:
            self.down[0] = self.down[-1]
            self.up[0] = self.up[-1]
            if self.data.low[0] < self.down[0]:
                self.trend = -1
                #self.signal[0] = -1
            if self.data.high[0] > self.up[0]:
                self.trend = 1
                #self.signal[0] = 1
        
            # if self.data.low[0] < self.highest_value - 1:
            #     self.down[0] = self.highest_value - 1
            #     print(self.down[0]-2)
            #     self.trend = -1
            pass
        
       
        
            
        #self.up[0] = max(max(self.data.close.get(ago=-1, size =3)), max(self.data.open.get(ago=-1, size =3)))
class MyStrategy(bt.Strategy):
    def __init__(self):
        print('hello new feature!!')
        print('hello new featur2e!!')
        print('INIT', self.data.open[0])
        MyIndicator(self.data)
    def start(self):
        print('START', self.data.open[0])

    def prenext(self):
        print('preNEXT', self.data.open[0])
       
    def nextstart(self):
        print('NEXTSTART', self.data.open[0])
    def next(self):
        print("A new bar    ", self.data.open[0] )
    
    def stop(self):
        print('STOP ok', self.data.open[0])
        
cerebro = bt.Cerebro()

dataframe = pd.read_csv("1daygold10sample.csv")
dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest'] = 0
bar_minute = bt.feeds.PandasData(dataname=dataframe,fromdate = datetime.datetime(2022, 1, 24), todate=datetime.datetime(2022, 1, 26))

#Add datafeed to cerebro
cerebro.adddata(bar_minute)

cerebro.addstrategy(MyStrategy)

cerebro.run()

cerebro.plot(style = 'candlestick')