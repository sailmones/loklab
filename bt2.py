# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import backtrader.indicators as btind
import pandas as pd
import numpy as np



class MyStrategy(bt.Strategy):
    def __init__(self):
        self.followIndicator = bt.indicators.FollowIndicator(self.data, spacePrice =2)
        self.buy_signal = bt.indicators.CrossOver(self.data.open, self.followIndicator.up)
        self.sell_signal = bt.indicators.CrossDown(self.data.open, self.followIndicator.down)
        print("init MyStrategy")
             
        self.followIndicator.plotinfo.plot = True
        self.buy_signal.plotinfo.plot = True
        self.sell_signal.plotinfo.plot = True
        
        
   
    def next(self):
        pass
        #print("A new Bar MyStrategy")
        
        # ma_value = self.bt_sma[0]
        # ma_value1 = self.bt_sma[1]
        
        # if self.data.close[0] > ma_value and self.data.close[-1] <= ma_value1:
        #     self.order = self.buy()
        # if self.data.close[0] > ma_value and self.data.close[-1] >= ma_value1:
        #     self.order = self.sell()
        #print(self.data.close[0])
        #print(self.data.close[0])
    
        # if not self.position and self.buy_sell_signal[0] == 1:
        #     self.order = self.buy()
        # if not self.position and self.buy_sell_signal[0] == -1:
        #     self.order = self.sell()    
        # if self.position and self.buy_sell_signal[0] == 1:
        #     pass
    def stop(self):
        print("Stop MyStrategy")

class FollowIndicator(bt.indicator):    
    lines = ("up", "down")
    params = (
        ('spacePrice', 2)
        # ('start', datetime.time(9, 10)),
        # ('end', datetime.time(17, 15)),
    )
    def __init__(self):
        #self.addminperiod(4)
        self.plotinfo.plotmaster = self.data
        
        self.dailyHigh = 0
        self.dailyLow = 0
        # tframe = self.data._timeframe
        # tcomp = self.data._compression
        # print("tframe:" , tframe )
        # print("tcomp:" , tcomp)
    def next(self):
        self.dailyHigh = max(self.dailyHigh, self.data.high[0])
        self.dailyLow = min(self.dailyLow, self.data.low[0])
        self.down[0]= self.dailyHigh - self.p.spacePrice
        self.up[0] = self.dailyLow + self.p.spacePrice
        # self.lines.down[0]= min(min(self.data.close.get(ago=-1, size=3)), min(self.data.open.get(ago= -1, size= 3))) 
if __name__ == '__main__':
    #1. Create a cerebro
    cerebro = bt.Cerebro(oldsync=False)
    #2. Add data feed
    #2.1 Create a data feed
    df = pd.read_csv("1daygold.csv")
    print(df)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['volume'] = 0
    df.set_index('datetime', inplace=True)
    brf_min_bar = bt.feeds.PandasData(dataname = df, 
                                      fromdate = datetime.datetime(2022,12,1), 
                                      todate=datetime.datetime(2022,3,10),
                                      timeframe=bt.TimeFrame.Minutes
                                      )
    cerebro.adddata(brf_min_bar)
    cerebro.addstrategy(MyStrategy)
    
    cerebro.addindicator(FollowIndicator, spacePrice = 2)
    #4. Run
    cerebro.run()

    #5. Plot rusult
    cerebro.plot(style="candle")