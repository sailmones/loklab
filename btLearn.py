import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import datetime
from backtrader.indicators import ExponentialMovingAverage as EMA



class MyStrategy(bt.Strategy):
    params = (
        ('ema_period', 10),
    )

    def __init__(self):
       self.ema = EMA(period=self.p.ema_period)

    def log(self, msg, dt=None):
        print("{} : {}".format(dt or self.datas[0].datetime.datetime(0), msg))
        
    def next(self):
        self.log('{} - {} {} @ {}'.format(self.datas[0].datetime.date(0), self.datas[0].close[0], self.datas[0]._name, self.ema[0]))
        if self.datas[0].close[0] < self.ema[0]:
            orders = [self.buy()]
            self.orders_ref = [order.ref for order in orders if order]

        if self.datas[0].close[0] > self.ema[0]:
            self.close()

    def notify_order(self, order):
        self.log('{} - {} {} @ {}'.format(order.data._name, order.size, order.data._name, order.price))
        if not order.alive() and order.ref in self.orders_ref:
            self.orders_ref.remove(order.ref)

    # def notify_trade(self, trade):
    #     self.log('{} - {} {} @ {}'.format(trade.dt.date(0), trade.size, trade.data._name, trade.price))


df = pd.read_csv("1daygold.csv")
print(df)
df['datetime'] = pd.to_datetime(df['datetime'])
df['volume'] = 0
df.set_index('datetime', inplace=True)
pandas_data = btfeeds.PandasData(dataname = df, fromdate = datetime.datetime(2022,1,5), todate=datetime.datetime(2022,3,10), timeframe=bt.TimeFrame.Minutes)



cerebro = bt.Cerebro()

cerebro.adddata(pandas_data, name= 'hello')
cerebro.addstrategy(MyStrategy, ema_period=10)
cerebro.run()





