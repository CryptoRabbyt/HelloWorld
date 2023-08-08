import pandas as pd
import numpy as np
import os
from datetime import datetime,timedelta
from pandas.tseries.offsets import Day,MonthBegin
from dateutil.parser import parse
import talib

###
# 读取CSV
# path:CSV的路径
# filename：CSV的文件名
###
def getStockData(path,filename):
    return pd.read_csv(path+filename,index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)

###
# 把原始数据转换为周期为“日”的数据
# stockData：包含了原始数据的DataFrame
###
def period2Day(stockData):

    stockDataByD = stockData.to_period('D')
    stockDataByD = stockDataByD[stockDataByD['收盘价']!=0]
    # 前复权
    stockDataByD['收盘价']=(stockDataByD['收盘价']*stockDataByD['总市值']/stockDataByD['收盘价'])/(stockDataByD['总市值'][0]/stockDataByD['收盘价'][0])
    stockDataByD['最高价']=(stockDataByD['最高价']*stockDataByD['总市值']/stockDataByD['最高价'])/(stockDataByD['总市值'][0]/stockDataByD['最高价'][0])
    stockDataByD['最低价']=(stockDataByD['最低价']*stockDataByD['总市值']/stockDataByD['最低价'])/(stockDataByD['总市值'][0]/stockDataByD['最低价'][0])
    stockDataByD['开盘价']=(stockDataByD['开盘价']*stockDataByD['总市值']/stockDataByD['开盘价'])/(stockDataByD['总市值'][0]/stockDataByD['开盘价'][0])

    # 过滤无用数据
    stockDataByD["收盘价"][stockDataByD["收盘价"]=='None'] = np.nan
    stockDataByD["最高价"][stockDataByD["最高价"]=='None'] = np.nan
    stockDataByD["最低价"][stockDataByD["最低价"]=='None'] = np.nan
    stockDataByD["开盘价"][stockDataByD["开盘价"]=='None'] = np.nan
    stockDataByD["换手率"][stockDataByD["换手率"]=='None'] = np.nan
    stockDataByD["总市值"][stockDataByD["总市值"]=='None'] = np.nan

    stockDataByD = stockDataByD[stockDataByD['收盘价'].notna()]
    stockDataByD = stockDataByD[stockDataByD['收盘价'] > 0.01]

    stockDataByD["收盘价"] = stockDataByD["收盘价"].astype('float')
    stockDataByD["最高价"] = stockDataByD["最高价"].astype('float')
    stockDataByD["最低价"] = stockDataByD["最低价"].astype('float')
    stockDataByD["开盘价"] = stockDataByD["开盘价"].astype('float')
    stockDataByD["换手率"] = stockDataByD["换手率"].astype('float')
    stockDataByD["总市值"] = stockDataByD["总市值"].astype('float')
    return stockDataByD

###
# 日期从取样中apply的聚合函数
# x：从取样传过来的DataFrame
###
def toMonthData(x):
    if(x.empty):
        return None
    else:
        return x.agg({'收盘价':lambda x: x[-1],'最高价':'max','最低价':'min','开盘价':lambda x: x[0],'换手率':'sum','总市值':lambda x: x[-1],'成交量':'count'})
###
# 把周期为“日”的数据转换为周期为“月”的数据
# stockDataByD：周期为“日”的数据
###
def period2Month(stockDataByD):

    stockDataByM = stockDataByD.resample('M').apply(toMonthData)
    # 无数据的月份也过滤掉
    stockDataByM = stockDataByM[stockDataByM['收盘价'].notna()]

    stockDataByM['涨幅']=stockDataByM['收盘价']/stockDataByM.shift(1)['收盘价']
    stockDataByM['sar'] = talib.SAR(stockDataByM['最高价'].values,stockDataByM['最低价'].values,acceleration=0.02, maximum=0.2)

    # macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    stockDataByM['macd'] = talib.MACD(stockDataByM['收盘价'])[0]

    
    # 添加下一月份的条目
    newRow=pd.DataFrame({'涨幅':1,'换手率':0,'成交量':0},index = [stockDataByM.index[-1]+1])
    # print(newRow)
    stockDataByM = stockDataByM.append(newRow)
    return stockDataByM

###
# 计算Macd中的EMA
# df：周期为“月”的数据
# N：计算前N个数据
###
def calc_EMA(df, N): 
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'收盘价']
        if i>0:
            df.ix[i,'ema']=((N-1)*df.ix[i-1,'ema']+2*df.ix[i,'收盘价'])/(N+1)
    ema=list(df['ema'])
    return ema

###
# 帮助周期为“月”的数据计算期Macd，并使其新增列['ema'],['diff'],['dea'],['macd']
# df：周期为“月”的数据
###
def calc_MACD(df, short=12, long=26, M=9):
    emas = calc_EMA(df, short)
    # print(pd.Series(emas))
    emaq = calc_EMA(df, long)
    # print(pd.Series(emaq))
    df['diff'] = (pd.Series(emas)-pd.Series(emaq)).values
    for i in range(len(df)):
        if i==0:
            df.ix[i,'dea'] = df.ix[i,'diff']  
        if i>0:  
            df.ix[i,'dea'] = ((M-1)*df.ix[i-1,'dea'] + 2*df.ix[i,'diff'])/(M+1)  
    df['macd'] = 2*(df['diff'] - df['dea'])

    # 添加下一月份的条目
    newRow=pd.DataFrame({'涨幅':100,'换手率':0,'成交量':0,'macd':100},index = [df.index[-1]+1])
    # print(newRow)
    df = df.append(newRow)
    return df

###
# 把Ser合并到Df中
# df：原来的df
# ser：要合并的Series
# columnName：合并之后新列的名字
###
def mergeSerToDf(df,ser,columnName):
    ser.name = columnName
    return pd.merge(df,ser,left_index=True,right_index=True, how="left")

###
# path：股票数据文件夹位置
# calStartDay：从哪天开始收益
# reserveDataMonths：计算收益需要使用前N前的数据
###
def aggDatas(path,calStartDay,reserveDataMonths):
    files = os.listdir(path)[:-1]

    rng = pd.period_range(parse(calStartDay)-MonthBegin()*reserveDataMonths, datetime.now().date()+MonthBegin(), freq='M')
    closePriceDf = pd.DataFrame(index=rng)
    rateDf = pd.DataFrame(index=rng)
    macdDf = pd.DataFrame(index=rng)
    turnOverDf = pd.DataFrame(index=rng)
    activeDaysDf = pd.DataFrame(index=rng)
    marketValueDf = pd.DataFrame(index=rng)
    sarDf = pd.DataFrame(index=rng)
    highPriceDf = pd.DataFrame(index=rng)
    lowPriceDf = pd.DataFrame(index=rng)

    dropStock_DataFew = 0
    dropStock_NoDataLately = 0
    dropStock_Error = 0
    stockCount = 0

    for filename in files:
        #计数
        stockCount += 1
        print(str(stockCount)+'--'+filename)


        try:
            # 读取CSV
            stockData = getStockData(path,filename)
            if(stockData.index[-1]>(parse(calStartDay)-MonthBegin()*(reserveDataMonths+1))):
                dropStock_DataFew += 1
                print(str(stockData.index[-1])+'--'+filename+'数据过少')
                continue
            elif((datetime.now()-stockData.index[0])>30*Day()):#最近没数据不要
                dropStock_NoDataLately+=1
                print(filename+'最近没数据')
                continue

            stockDataByD = period2Day(stockData)
            stockDataByM = period2Month(stockDataByD)
        # stockDataMACD = calc_MACD(stockDataByM)
        except:
            dropStock_Error += 1
            print(filename+'由于报错处理不了')
            continue

        closePriceDf = mergeSerToDf(closePriceDf,stockDataByM['收盘价'],'c-'+filename.split('.')[0])
        rateDf = mergeSerToDf(rateDf,stockDataByM['涨幅'],'c-'+filename.split('.')[0])
        macdDf = mergeSerToDf(macdDf,stockDataByM['macd'],'c-'+filename.split('.')[0])
        turnOverDf = mergeSerToDf(turnOverDf,stockDataByM['换手率'],'c-'+filename.split('.')[0])
        activeDaysDf = mergeSerToDf(activeDaysDf,stockDataByM['成交量'],'c-'+filename.split('.')[0])
        marketValueDf = mergeSerToDf(marketValueDf,stockDataByM['总市值'],'c-'+filename.split('.')[0])
        sarDf = mergeSerToDf(sarDf,stockDataByM['sar'],'c-'+filename.split('.')[0])
        highPriceDf = mergeSerToDf(highPriceDf,stockDataByM['最高价'],'c-'+filename.split('.')[0])
        lowPriceDf = mergeSerToDf(lowPriceDf,stockDataByM['最低价'],'c-'+filename.split('.')[0])
        # pd.merge(closePriceDf,stockDataMACD['收盘价'],left_index=True,right_index=True, how="left",suffixes=("",filename.split('.')[0]))
        # rateDf = pd.merge(rateDf,stockDataMACD['涨幅'],left_index=True,right_index=True, how="left",suffixes=("",filename.split('.')[0]))
        # macdDf = pd.merge(macdDf,stockDataMACD['macd'],left_index=True,right_index=True, how="left",suffixes=("",filename.split('.')[0]))
        # turnOverDf = pd.merge(turnOverDf,stockDataMACD['换手率'],left_index=True,right_index=True, how="left",suffixes=("",filename.split('.')[0]))
        # activeDaysDf = pd.merge(activeDaysDf,stockDataMACD['成交量'],left_index=True,right_index=True, how="left",suffixes=("",filename.split('.')[0]))

    if(not os.path.exists('Data/OperationTable'+calStartDay)):
        os.makedirs('Data/OperationTable'+calStartDay)

    closePriceDf.to_csv('Data/OperationTable'+calStartDay+'/1.closePriceDf.csv',encoding='gbk')
    rateDf.to_csv('Data/OperationTable'+calStartDay+'/2.rateDf.csv',encoding='gbk')
    macdDf.to_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',encoding='gbk')
    turnOverDf.to_csv('Data/OperationTable'+calStartDay+'/4.turnOverDf.csv',encoding='gbk')
    activeDaysDf.to_csv('Data/OperationTable'+calStartDay+'/5.activeDaysDf.csv',encoding='gbk')
    marketValueDf.to_csv('Data/OperationTable'+calStartDay+'/6.marketValueDf.csv',encoding='gbk')
    sarDf.to_csv('Data/OperationTable'+calStartDay+'/7.sarDf.csv',encoding='gbk')
    highPriceDf.to_csv('Data/OperationTable'+calStartDay+'/8.highPriceDf.csv',encoding='gbk')
    lowPriceDf.to_csv('Data/OperationTable'+calStartDay+'/9.lowPriceDf.csv',encoding='gbk')

    print('因数据过太少而弃用的数据：'+str(dropStock_DataFew))
    print('因无最近数据过太而弃用的数据：'+str(dropStock_NoDataLately))
    print('因报错而弃用的数据：'+str(dropStock_Error))