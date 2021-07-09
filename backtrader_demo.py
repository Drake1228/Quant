#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 18:04:59 2021

@author: delizhu
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)

    
#cerebro = bt.Cerebro(**kwargs)#创建Cerebro框架
#cerebro.addstrategy(MyStrategy,mypara1,mypara2)#增添交易策略
#
###增添其他元素
##.addwriter 
##.addanalyzer
##.addobserver
#
###改变broker
#cerebro.broker = broker
#
##接受通知
#cerebro.notify_store
#
##运行Cerebro
#result = cerebro.run(**kwargs)
#cerebro.plot()

import datetime
import backtrader as bt

class StrategyClass(bt.Strategy):
    def __init__(self):
        self.sma = bt.ind.SMA(period = 15)
    #指标必须要定义在策略类中的初始化函数中 !!!!
    #sma源码位于indicators\sma.py
        #self.wma = bt.ind.WeightedMovingAverage(period = 15)    
    
    def next(self):
        #移动平均线
        #self.data.close 收盘价
        #收盘价大于sma均线，买入，反之卖出
        if self.data.close > self.sma:
            self.buy()
        if self.data.close <= self.sma:
            self.sell()
        ##加权移动平均WeightedMovingAverage
#        if self.data.close > self.wma:
#            self.buy()
#        if self.data.close <= self.wma:
#            self.sell()
        
    
cerebro=bt.Cerebro()
#datapath="/Users/delizhu/Desktop/Quant trading System/Tre10y.xls"
data = bt.feeds.GenericCSVData(dataname = 'Tre10y.csv' ,
                             fromdate = datetime.datetime(2018, 1, 1),
                             todate = datetime.datetime(2020, 3, 20),
                             nullvalue=0.0,
                             dtformat=('%Y-%m-%d'),
                             datetime=0,
                             high=3,
                             low=4,
                             open=1,
                             close=2,
                             volume=5,
                             openinterest=-1)

cerebro.adddata(data)
cerebro.addstrategy(StrategyClass)
cerebro.broker.set_cash(200000)
cerebro.run(maxcpu=1)
cerebro.plot()




            
        