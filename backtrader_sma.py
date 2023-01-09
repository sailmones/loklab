# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import matplotlib.pyplot as plot
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.bt_sma = bt.indicators.MovingAverageSimple(self.data, period=124)
        self.buy_sell_signal = bt.indicators.CrossOver(self.data.open, self.bt_sma)
        print("init MyStrategy")
        
        tname = self.data1._name
        tframe = self.data1._timeframe
        tcomp = self.data1._compression
        ind = bt.TimeFrame.Minutes
        print("index:" , ind)
        print("tframe:" , tframe )
        print("tcomp:" , tcomp)
        print("tname:" , tname)
        tname = self.data._name
        tframe = self.data._timeframe
        tcomp = self.data._compression
        ind = bt.TimeFrame.Days
        print("index:" , ind)
        print("tframe:" , tframe )
        print("tcomp:" , tcomp)
        print("tname:" , tname)
        
        #self.bt_sma.plotinfo.plot = False
        #self.buy_sell_signal.plotinfo.plot = False

    def start(self):
        print("Starting MyStrategy")
    def prenext(self):
        print("Prenext MyStrategy")
    def nextstart(self):
        #print("NextStart MyStrategy")
        pass
    def next(self):
        #print("A new Bar MyStrategy")
        
        # ma_value = self.bt_sma[0]
        # ma_value1 = self.bt_sma[1]
        
        # if self.data.close[0] > ma_value and self.data.close[-1] <= ma_value1:
        #     self.order = self.buy()
        # if self.data.close[0] > ma_value and self.data.close[-1] >= ma_value1:
        #     self.order = self.sell()
        #print(self.data.close[0])
        #print(self.data.close[0])
    
        if not self.position and self.buy_sell_signal[0] == 1:
            self.order = self.buy()
        if not self.position and self.buy_sell_signal[0] == -1:
            self.order = self.sell()    
        if self.position and self.buy_sell_signal[0] == 1:
            pass
    def stop(self):
        print("Stop MyStrategy")


# 6 indicators custom
# class three_bars(bt.indicator):    
#     lines = ("up", "down",)
#     def __init__(self):
#         self.addminperiod(4)
#         self.plotinfo.plotmaster = self.data
#         # tframe = self.data._timeframe
#         # tcomp = self.data._compression
#         # print("tframe:" , tframe )
#         # print("tcomp:" , tcomp)
#     def next(self):
#         self.lines.up[0] = max(max(self.data.close.get(ago = -1, size = 3)),max (self.data.open.get(ago=-1, size=3)))
#         self.lines.down[0]= min(min(self.data.close.get(ago=-1, size=3)), min(self.data.open.get(ago= -1, size= 3)))

# class MyStrategy2(bt.Strategy):
#     def __init__(self):
#         self.up_down = three_bars(self.data)
#         self.buy_signal = bt.indicators.CrossOver(self.data.close,self.up_down.up)
#         self.sell_signal = bt.indicators.CrossDown(self.data.close, self.up_down.down)
        
#         self.buy_signal.plotinfo.plot = False
#         self.sell_signal.plotinfo.plot = False
#         self.up_down.plotinfo.plot = False
#     def next(self):
#         if not self.position and self.buy_signal[0] == 1:
#             self.order = self.buy()
#         if self.getposition().size < 0 and self.buy_signal[0] ==1:
#             self.order = self.close()
#             self.order = self.buy()
#         if not self.position and self.sell_signal[0] == 1:
#             self.order = self.sell()
#         if self.getposition().size < 0 and self.sell_signal[0] == 1:
#             self.order = self.close()
#             self.order = self.sell()
            
            
            
if __name__ == "__main__":
    #1. create cerebro
    cerebro = bt.Cerebro()

    #2. Add datafeed
    #2.1 Create a data feed
    df = pd.read_csv("1daygold.csv")
    print(df)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['volume'] = 0
    df.set_index('datetime', inplace=True)
    brf = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2022,1,5), todate=datetime.datetime(2022,3,10), timeframe=bt.TimeFrame.Minutes)

    #2.1.2 Create a csv data feed
    # brf = bt.feeds.GenericCSVData(
    #     dataname = "my_historical_data.csv",
    #     nullvalue = 0.0,
    #     dtformat =('%Y-%m-%d %H:%M:%S'),    
    #     datetime=0,
    #     high=2,
    #     low=3,    
    #     open=1,    
    #     close=4,
    #     volume=5,
    #     openinterest=-1
    # )

    #2.2 Add the Data Feed to Cerebro
    cerebro.adddata(brf)
    cerebro.resampledata(brf, timeframe=bt.TimeFrame.Days)
    #3. Add strategy
    cerebro.addstrategy(MyStrategy)
    
    #4. Run
    cerebro.run()

    #5. Plot rusult
    cerebro.plot(style="candle")
    
