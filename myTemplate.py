# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

class MyIndicator(bt.Indicator):
    pass

cerebro = bt.Cerebro()

dataframe = pd.read_csv("1daygold10sample.csv")
dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest'] = 0
bar_minute = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2022, 1, 24), todate=datetime.datetime(2022, 2, 4))


cerebro.adddata(bar_minute)
cerebro.addstrategy()
cerebro.run()
cerebro.plot()