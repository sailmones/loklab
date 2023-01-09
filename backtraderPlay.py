from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import datetime
import math
import pandas as pd

import backtrader as bt


def time2num(tm):
    """
    Convert :mod:`time` to the to the preserving hours, minutes, seconds
    and microseconds.  Return value is a :func:`float`.
    """
    HOURS_PER_DAY = 24.0
    MINUTES_PER_HOUR = 60.0
    SECONDS_PER_MINUTE = 60.0
    MUSECONDS_PER_SECOND = 1e6
    MINUTES_PER_DAY = MINUTES_PER_HOUR * HOURS_PER_DAY
    SECONDS_PER_DAY = SECONDS_PER_MINUTE * MINUTES_PER_DAY
    MUSECONDS_PER_DAY = MUSECONDS_PER_SECOND * SECONDS_PER_DAY

    tm_num = (tm.hour / HOURS_PER_DAY +
              tm.minute / MINUTES_PER_DAY +
              tm.second / SECONDS_PER_DAY +
              tm.microsecond / MUSECONDS_PER_DAY)

    return tm_num


def dtime_dt(dt):
    return math.trunc(dt)


def dtime_tm(dt):
    return math.modf(dt)[0]

    
    
    
    
class RelativeVolumeByBar(bt.Indicator):
    alias = ('RVBB',)
    lines = ('rvbb',)

    params = (
        ('prestart', datetime.time(8, 00)),
        ('start', datetime.time(9, 10)),
        ('end', datetime.time(17, 15)),
    )

    def _plotlabel(self):
        plabels = []
        for name, value in self.params._getitems():
            plabels.append('%s: %s' % (name, value.strftime('%H:%M')))

        return plabels
    
    def __init__(self):
        # Inform the platform about the minimum period needs
        minbuffer = self._calcbuffer()
        self.addminperiod(minbuffer)

        # Structures/variable to keep synchronization
        self.pvol = dict()
        self.vcount = collections.defaultdict(int)

        self.days = 0
        self.dtlast = 0

        # Keep the start/end times in numeric format for comparison
        self.start = time2num(self.p.start)
        self.end = time2num(self.p.end)

        # Done after calc to ensure coop inheritance and composition work
        super(RelativeVolumeByBar, self).__init__()

    def _barisvalid(self, tm):
        return self.start <= tm <= self.end

    def _daycount(self):
        dt = dtime_dt(self.data.datetime[0])
        if dt > self.dtlast:
            self.days += 1
            self.dtlast = dt

    def prenext(self):
        self._daycount()

        tm = dtime_tm(self.data.datetime[0])
        if self._barisvalid(tm):
            self.pvol[tm] = self.data.volume[0]
            self.vcount[tm] += 1

    def next(self):
        self._daycount()

        tm = dtime_tm(self.data.datetime[0])
        if not self._barisvalid(tm):
            return

        # Record the "minute/second" of this day has been seen
        self.vcount[tm] += 1

        # Get the bar's volume
        vol = self.data.volume[0]

        # If number of days is right, we saw the same "minute/second" last day
        if self.vcount[tm] == self.days:
            self.lines.rvbb[0] = vol / self.pvol[tm]

        # Synchronize the days and volume count for next cycle
        self.vcount[tm] = self.days

        # Record the volume for this bar for next cycle
        self.pvol[tm] = vol

    def _calcbuffer(self):
        # Period calculation
        minend = self.p.end.hour * 60 + self.p.end.minute
        # minstart = session_start.hour * 60 + session_start.minute
        # use prestart to account for market_data
        minstart = self.p.prestart.hour * 60 + self.p.prestart.minute

        minbuffer = minend - minstart

        tframe = self.data._timeframe
        tcomp = self.data._compression
        ind = bt.TimeFrame.Seconds.index
        print(ind)
        if tframe == bt.TimeFrame.Seconds:
            minbuffer = (minbuffer * 60)

        minbuffer = (minbuffer // tcomp) + tcomp

        return minbuffer
    
 