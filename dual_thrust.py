# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import backtrader.indicators as btind
import pandas as pd
import numpy as np


class r_s(bt.Strategy):
    def __init__(self):
        print('death')    
        self.data1.plotinfo.plot = False   
if __name__ == '__main__':
    #1. Create a cerebro
    cerebro = bt.Cerebro(oldsync=False)
    #2. Add data feed
    #2.1 Create a data feed
    df = pd.read_csv("my_historical_data4.csv")
    print(df)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['volume'] = 0
    df.set_index('datetime', inplace=True)
    brf_min_bar = bt.feeds.PandasData(dataname = df, 
                                      fromdate = datetime.datetime(2022,3,5), 
                                      todate=datetime.datetime(2022,3,10),
                                      timeframe=bt.TimeFrame.Minutes
                                      )
    
    #2.2 Add the Data Feed to Cerebro
    cerebro.adddata(brf_min_bar)
    cerebro.resampledata(brf_min_bar, timeframe=bt.TimeFrame.Days)
    
    #3 Add Strategy
    cerebro.addstrategy(r_s)
    #4 Run Strategy
    cerebro.run()
    #5 Plot result
    cerebro.plot()