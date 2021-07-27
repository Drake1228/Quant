#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 16:40:02 2021

@author: delizhu
"""
from pandas_datareader import data as pdr 
import yfinance as yf 
yf.pdr_override() 
 
# Plotting graphs 
import matplotlib.pyplot as plt
#import seaborn 
import talib as ta

 
# Data manipulation 
import numpy as np 
import pandas as pd

stock = pdr.get_data_yahoo("^NSEI",start = '2015-01-03', end = '2020-12-30')

stock['high_10'] = stock.Close.shift(1).rolling(window=10).max()#10日最大
stock['low_10'] = stock.Close.shift(1).rolling(window=10).min()#10日最小
stock['avg_10'] = stock.Close.shift(1).rolling(window=10).mean()#10日均线

stock['high_5'] = stock.Close.shift(1).rolling(window=5).max()#5日最大
stock['low_5'] = stock.Close.shift(1).rolling(window=5).min()#5日最小
stock['avg_5'] = stock.Close.shift(1).rolling(window=5).mean()#5日均线

stock['RSI_9'] = ta.RSI(np.array(stock['Close']),timeperiod = 9)#9日MSI均线
stock['dif'], stock['dea'],stock['hist'] = ta.MACD(stock['Close'])# MACD 指标计算
# 计算EMA12和EMA26
stock['ema12'] = ta.EMA(stock['Close'], 12)
stock['ema26'] = ta.EMA(stock['Close'], 26)



##---------------利用均值判断标准------------------------
stock['long_entry'] = (stock.Close > stock.high_10) & (stock.Close > stock.high_5)
stock['short_entry'] = (stock.Close < stock.low_5) & (stock.Close < stock.low_5)
#出场信号
stock['long_exit'] = (stock.Close < stock.avg_10) | (stock.Close < stock.avg_5)
stock['short_exit'] = (stock.Close > stock.avg_10) |(stock.Close > stock.avg_5)



#position统一信号
stock['positions_long'] = np.nan 
stock.loc[stock.long_entry,'positions_long']= 1 
stock.loc[stock.long_exit,'positions_long']= 0 

stock['positions_short'] = np.nan 
stock.loc[stock.short_entry,'positions_short']= -1 
stock.loc[stock.short_exit,'positions_short']= 0 
#stock = stock.fillna(0)

stock['Signal'] = stock.positions_long + stock.positions_short 
#stock = stock.fillna(0)

##----------------MACD判断标准--------------------

#下列的 signal 1均为long进场信号,-1为short进场信号，0为清仓出场信号 一轮交易结束
# sig1只考虑HIST指标，HIST转正时开仓买入，转负时清仓
stock['sig1_L'] = ((stock['hist']>0) & (stock['Close']>stock['ema26'])).astype(int)#做多信号

stock['sig1_S'] = -((stock['hist']<0) & (stock['dea']<0)).astype(int)#做空信号
# sig2同时考虑HIST指标和DEA指标，只有当HIST转正，且DEA在0以上时，才开仓买入，任何一个指标变负即清仓。
#stock['sig2'] = (stock['hist']>0) & (stock['dea']>0)
# sig3同时考虑HIST和EMA指标，只有当HIST为正，而且当前价格在慢线（26日指数加权平均价）上方时，才开仓买入，任何一个指标转负即清仓。
#stock['sig3'] = (stock['hist']>0) & (stock['Close']>stock['ema26'])

##---------------RSI上穿20价格反弹抄底---------------
stock['sig2_rsi'] = ((stock['RSI_9'].shift(1)>20)&(stock['RSI_9']<20)).astype(int)


data_export = stock[['High','Low','Close','Signal','sig1_L','sig1_S','sig2_rsi']]
data_export.to_excel(r'/Users/delizhu/Desktop/Quant/data_for_train2.xlsx')




#plt.figure(figsize=(10,8))
#ax1=plt.subplot(4,1,1)
#ax1.plot(stock['Close'], label = 'Close price')
#ax2=plt.subplot(4,1,2)
#ax2.plot(stock['dif'],label = 'Diff')
#ax2.plot(stock['dea'],color ='r',label = 'MACD')
#ax3=plt.subplot(4,1,3)
#ax3.bar(x=stock['sig1_S'].index, height=stock['sig1_S'].values)
#ax4=plt.subplot(4,1,4)
#ax4.bar(x=stock['Signal'].index, height=stock['Signal'].values)
#plt.show()
