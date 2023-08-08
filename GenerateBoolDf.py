import pandas as pd
import numpy as np
import FiltAndAnalyseMethod as fam

### 弃用
# 如果某月份的前3个月，MACD连续上涨，则保存为True
###
def genIsMacdRiseCsv(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)>macdDf.shift(2)
    b = macdDf.shift(2)>macdDf.shift(3)
    isMacdRiseDf = a&b
    isMacdRiseDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD连涨.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD连续下跌，则保存为True
###
def genIsMacdFallCsv(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)<macdDf.shift(2)
    b = macdDf.shift(2)<macdDf.shift(3)
    isMacdFallDf = a&b
    isMacdFallDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD连跌.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD先上升后下跌，则保存为True
###
def genIsMacdRiseAndFallCsv(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)<macdDf.shift(2)
    b = macdDf.shift(2)>macdDf.shift(3)
    isMacdFallDf = a&b
    isMacdFallDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD转跌.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD先上升后下跌，则保存为True
###
def genIsMacdFallAndRiseCsv(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)>macdDf.shift(2)
    b = macdDf.shift(2)<macdDf.shift(3)
    isMacdFallDf = a&b
    isMacdFallDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD转升.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD先上升后下跌，则保存为True
###
def genIsMacdTrendUp(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = (macdDf.shift(1)-macdDf.shift(2))>(macdDf.shift(2)-macdDf.shift(3))
    isMacdTrendUp = a
    isMacdTrendUp.to_csv('Data/OperationTable'+calStartDay+'/b-MACD趋势上升.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD连续下跌，则保存为True
###
def genIsMacdFallCsv(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)<macdDf.shift(2)
    b = macdDf.shift(2)<macdDf.shift(3)
    isMacdFallDf = a&b
    isMacdFallDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD连跌.csv',encoding='gbk')

###
# 生成SAR各月份的趋势
# weight：更偏向于选择哪一种趋势的股票？
###
def genMacdSpreadDf(calStartDay):
    isMacdRiseDf = fam.readCsv(calStartDay,'b-MACD连涨')
    isMacdFallDf = fam.readCsv(calStartDay,'b-MACD连跌')

    macdSpreadDf = pd.DataFrame({'Macd连涨趋势':isMacdRiseDf[isMacdRiseDf==True].count(axis=1),
                                'Macd连跌趋势':isMacdFallDf[isMacdFallDf==True].count(axis=1)})

    # 更偏向于选择哪一种趋势的股票？
    # weight = [1,1,1,1]
    trendAvgPerDf = macdSpreadDf/macdSpreadDf.mean()
    trendAvgPerDf.columns = ['平均比--Macd连涨趋势','平均比--Macd连跌趋势']
    # serMaxIdx = pd.Series(macdSpreadDf.values.argmax(axis = 1,),index = macdSpreadDf.index)
    serMaxIdx = pd.Series(index = macdSpreadDf.index)
    serMaxIdx.name = '趋势类型'
    serMaxIdx[:] = 0
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > -(macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.8
    serMaxIdx[boolDf] = 1
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > -(macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.6
    serMaxIdx[boolDf] = 2
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > -(macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.4
    serMaxIdx[boolDf] = 3
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > -(macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.2
    serMaxIdx[boolDf] = 4
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > (macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.2
    serMaxIdx[boolDf] = 5
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > (macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.4
    serMaxIdx[boolDf] = 6
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > (macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.6
    serMaxIdx[boolDf] = 7
    boolDf = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > (macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.8
    serMaxIdx[boolDf] = 8
    # a = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) < (macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.2
    # b = (macdSpreadDf['Macd连涨趋势']-macdSpreadDf['Macd连跌趋势']) > -(macdSpreadDf['Macd连涨趋势']+macdSpreadDf['Macd连跌趋势'])*0.2
    # serMaxIdx[a&b] = 2
    # serMaxIdx_Weight = pd.Series((trendAvgPerDf*weight).values.argmax(axis = 1,),index = trendAvgPerDf.index)
    # serMaxIdx_Weight.name = '趋势类型(加权'

    macdSpreadDf = pd.merge(macdSpreadDf,trendAvgPerDf,left_index=True,right_index=True)
    macdSpreadDf = pd.merge(macdSpreadDf,serMaxIdx,left_index=True,right_index=True)
    # macdSpreadDf = pd.merge(macdSpreadDf,serMaxIdx_Weight,left_index=True,right_index=True)
    
    
    macdSpreadDf.to_csv('Data/OperationTable'+calStartDay+'/b-macd趋势分布.csv',encoding='gbk')

### 弃用
# 如果某月份的前3个月，MACD先上升后下跌，则保存为True
###
def genIsMacdEqu(calStartDay):
    macdDf = pd.read_csv('Data/OperationTable'+calStartDay+'/3.macdDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    macdDf = macdDf.to_period('M')
    a = macdDf.shift(1)==macdDf.shift(2)
    isMacdFallDf = a
    isMacdFallDf.to_csv('Data/OperationTable'+calStartDay+'/b-MACD平.csv',encoding='gbk')


### 弃用
# 如果某月份的前3个月，换手率增量逐步提升，则保存为True
###
def genIsTurnOverRise(calStartDay):
    turnOverDf = pd.read_csv('Data/OperationTable'+calStartDay+'/4.turnOverDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    activeDaysDf = pd.read_csv('Data/OperationTable'+calStartDay+'/5.activeDaysDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    turnOverDf = turnOverDf.to_period('M')
    activeDaysDf = activeDaysDf.to_period('M')

    # 日均换手率
    turnOverDf_ByMonth = turnOverDf/activeDaysDf
    # turnOverDf_ByMonth[turnOverDf_ByMonth==np.inf] = np.nan
    # turnOverDf_ByMonth[turnOverDf_ByMonth==-np.inf] = np.nan
    isTurnOverRiseDf = (turnOverDf_ByMonth.shift(1)-turnOverDf_ByMonth.shift(2))>(turnOverDf_ByMonth.shift(2)-turnOverDf_ByMonth.shift(3))

    isTurnOverRiseDf.to_csv('Data/OperationTable'+calStartDay+'/b-换手率增量上升.csv',encoding='gbk')

### 弃用
# 如果某月份的前3月换手率平均值介于前N个月平均值的某个范围之间，则保存为True
# limit_low：下限
# limit_high：上限
# month：前N个月
###
def genIsTurnOverBetween(calStartDay,limit_low,limit_high,month):
    turnOverDf = pd.read_csv('Data/OperationTable'+calStartDay+'/4.turnOverDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    activeDaysDf = pd.read_csv('Data/OperationTable'+calStartDay+'/5.activeDaysDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    turnOverDf = turnOverDf.to_period('M')
    activeDaysDf = activeDaysDf.to_period('M')

    # 近3月月均换手率
    averageTurnOverLast3Month_ByMonth = (turnOverDf.shift(1)+turnOverDf.shift(2)+turnOverDf.shift(3))/(activeDaysDf.shift(1)+activeDaysDf.shift(2)+activeDaysDf.shift(3))

    # 近N月换手率总和
    turnOverLastNMonth_Sum = turnOverDf.shift(1)
    activeDaysLastNMonth_Sum = activeDaysDf.shift(1)

    for i in range(2,month):
        turnOverLastNMonth_Sum += turnOverDf.shift(i)
        activeDaysLastNMonth_Sum += activeDaysDf.shift(i)

    # 近N月月均换手率
    averageTurnOverLastNMonth_ByMonth = turnOverLastNMonth_Sum/activeDaysLastNMonth_Sum

    a = averageTurnOverLast3Month_ByMonth>(limit_low*averageTurnOverLastNMonth_ByMonth)
    b = averageTurnOverLast3Month_ByMonth<(limit_high*averageTurnOverLastNMonth_ByMonth)
    isTurnOverBetweenDf = a&b
        
    isTurnOverBetweenDf.to_csv('Data/OperationTable'+calStartDay+'/b-前3月换手率介于前'+str(month)+'月'+str(limit_low)+'-'+str(limit_high)+'.csv',encoding='gbk')


###
# 如果某月份的前3月收盘价，转手率，活跃天数，SAR都不为空，则保存为True
###
def genIsMonthPass(calStartDay):
    closePriceDf = fam.readCsv(calStartDay,'1.closePriceDf')
    turnOverDf = fam.readCsv(calStartDay,'4.turnOverDf')
    activeDaysDf = fam.readCsv(calStartDay,'5.activeDaysDf')
    marketValueDf = fam.readCsv(calStartDay,'6.marketValueDf')
    sarDf = fam.readCsv(calStartDay,'7.sarDf')

    a = (closePriceDf.shift(1)!=np.nan)
    b = (closePriceDf.shift(2)!=np.nan)
    c = (closePriceDf.shift(3)!=np.nan)
    d = (turnOverDf.shift(1)!=np.nan)
    e = (turnOverDf.shift(2)!=np.nan)
    f = (turnOverDf.shift(3)!=np.nan)
    g = (activeDaysDf.shift(1)!=np.nan)
    h = (activeDaysDf.shift(2)!=np.nan)
    i = (activeDaysDf.shift(3)!=np.nan)
    j = (marketValueDf.shift(1)!=np.nan)
    k = (sarDf.shift(1)!=np.nan)
    l = (sarDf.shift(2)!=np.nan)
    m = (sarDf.shift(3)!=np.nan)

    isMonthPassDf = a&b&c&d&e&f&g&h&i&j&k&l&m

    isMonthPassDf.to_csv('Data/OperationTable'+calStartDay+'/b-该月份所有数据及格.csv',encoding='gbk')

###
# 如果某月份的前1个月市值大于某值，则保存为True
###
def genIsMarketValueGt(calStartDay,limit_low):
    marketValueDf = pd.read_csv('Data/OperationTable'+calStartDay+'/6.marketValueDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    marketValueDf = marketValueDf.to_period('M')


    genIsMarketValueGt = marketValueDf.shift(1)>limit_low
        
    genIsMarketValueGt.to_csv('Data/OperationTable'+calStartDay+'/b-上1月市值大于N亿.csv',encoding='gbk')

def marketValueQcut(x):
    try:
        return pd.qcut(x,16,labels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    except:
        x[:]=np.nan
        return x

###
# 把某月份的市值划分为6个区间，并保存起来
###
def genTurnOverPerDayRange(calStartDay):
    turnOverDf = fam.readCsv(calStartDay,'4.turnOverDf')
    activeDaysDf = fam.readCsv(calStartDay,'5.activeDaysDf')

    turnOverPerDayDf = (turnOverDf / activeDaysDf).shift(1)

    # marketValueDf = marketValueDf.shift(1)[genIsMarketValueGt]

    turnOverPerDayRangeDf = turnOverPerDayDf.transform(marketValueQcut,axis=1)

    turnOverPerDayRangeDf.to_csv('Data/OperationTable'+calStartDay+'/type-平均每日换手所属区间.csv',encoding='gbk')

###
# 把某月份的换手率划分为8个区间，并保存起来
###
def genMarketValueRange(calStartDay):
    marketValueDf = fam.readCsv(calStartDay,'6.marketValueDf')
    genIsMarketValueGt = fam.readCsv(calStartDay,'b-上1月市值大于N亿')

    marketValueDf = marketValueDf.shift(1)[genIsMarketValueGt]

    marketValueRangeDf = marketValueDf.transform(marketValueQcut,axis=1)

    marketValueRangeDf.to_csv('Data/OperationTable'+calStartDay+'/type-市值所属区间.csv',encoding='gbk')



###
# 根据SAR技术曲线，把股票趋势划分成4个阶段。股票当月份属于哪个阶段，分别用4个布尔CSV保存起来。
###
def genTrendBoolDf(calStartDay):
    closePriceDf = fam.readCsv(calStartDay,'1.closePriceDf')
    sarDf = fam.readCsv(calStartDay,'7.sarDf')

    dValueDf = closePriceDf-sarDf

    # 上涨形成趋势
    priceRiseFormDf = (dValueDf.shift(1)>0) & (dValueDf.shift(1)>dValueDf.shift(2))
    # 上涨停滞趋势
    priceRiseStagnateDf = (dValueDf.shift(1)>0) & (dValueDf.shift(1)<dValueDf.shift(2))
    # 下跌形成趋势
    priceFallFormDf = (dValueDf.shift(1)<0) & (dValueDf.shift(1)<dValueDf.shift(2))
    #下跌停滞趋势
    priceFallStagnateDf = (dValueDf.shift(1)<0) & (dValueDf.shift(1)>dValueDf.shift(2))

    priceRiseFormDf.to_csv('Data/OperationTable'+calStartDay+'/b-sar上涨形成趋势.csv',encoding='gbk')
    priceRiseStagnateDf.to_csv('Data/OperationTable'+calStartDay+'/b-sar上涨停滞趋势.csv',encoding='gbk')
    priceFallFormDf.to_csv('Data/OperationTable'+calStartDay+'/b-sar下跌形成趋势.csv',encoding='gbk')
    priceFallStagnateDf.to_csv('Data/OperationTable'+calStartDay+'/b-sar下跌停滞趋势.csv',encoding='gbk')

###
# 生成SAR各月份的趋势
# weight：更偏向于选择哪一种趋势的股票？
###
def genTrendSpreadDf(calStartDay,weight):
    priceRiseFormDf = fam.readCsv(calStartDay,'b-sar上涨形成趋势')
    priceRiseStagnateDf = fam.readCsv(calStartDay,'b-sar上涨停滞趋势')
    priceFallFormDf = fam.readCsv(calStartDay,'b-sar下跌形成趋势')
    priceFallStagnateDf = fam.readCsv(calStartDay,'b-sar下跌停滞趋势')


    
    trendSpreadDf = pd.DataFrame({'sar上涨形成趋势':priceRiseFormDf[priceRiseFormDf==True].count(axis=1),
                                'sar上涨停滞趋势':priceRiseStagnateDf[priceRiseStagnateDf==True].count(axis=1),
                                'sar下跌形成趋势':priceFallFormDf[priceFallFormDf==True].count(axis=1),
                                'sar下跌停滞趋势':priceFallStagnateDf[priceFallStagnateDf==True].count(axis=1)})

    # 更偏向于选择哪一种趋势的股票？
    # weight = [1,1,1,1]
    trendAvgPerDf = trendSpreadDf/trendSpreadDf.mean()
    trendAvgPerDf.columns = ['平均比--上涨形成','平均比--上涨停滞','平均比--下跌形成','平均比--下跌停滞']
    serMaxIdx = pd.Series(trendAvgPerDf.values.argmax(axis = 1,),index = trendAvgPerDf.index)
    serMaxIdx.name = '趋势类型'
    serMaxIdx_Weight = pd.Series((trendAvgPerDf*weight).values.argmax(axis = 1,),index = trendAvgPerDf.index)
    serMaxIdx_Weight.name = '趋势类型(加权'

    trendSpreadDf = pd.merge(trendSpreadDf,trendAvgPerDf,left_index=True,right_index=True)
    trendSpreadDf = pd.merge(trendSpreadDf,serMaxIdx,left_index=True,right_index=True)
    trendSpreadDf = pd.merge(trendSpreadDf,serMaxIdx_Weight,left_index=True,right_index=True)
    
    
    trendSpreadDf.to_csv('Data/OperationTable'+calStartDay+'/b-sar趋势分布.csv',encoding='gbk')

###
# 根据前3月收盘价形态，把股票8个收盘价形态。股票当月份属于哪个阶段，分别用4个布尔CSV保存起来。
###
def genPriceFormBoolDf(calStartDay):
    closePriceDf = fam.readCsv(calStartDay,'1.closePriceDf')

    # 形态1：跌后急涨
    closePriceForm1 = (closePriceDf.shift(1)>closePriceDf.shift(3)) & (closePriceDf.shift(3)>closePriceDf.shift(2))
    # 形态2：跌后缓涨
    closePriceForm2 = (closePriceDf.shift(3)>closePriceDf.shift(1)) & (closePriceDf.shift(1)>closePriceDf.shift(2))
    # 形态3：跌后缓跌
    closePriceForm3 = (closePriceDf.shift(3)>closePriceDf.shift(2)) & (closePriceDf.shift(2)>closePriceDf.shift(1)) & ((closePriceDf.shift(3)-closePriceDf.shift(2))>(closePriceDf.shift(2)-closePriceDf.shift(1)))
    # 形态4：跌后急跌
    closePriceForm4 = (closePriceDf.shift(3)>closePriceDf.shift(2)) & (closePriceDf.shift(2)>closePriceDf.shift(1)) & ((closePriceDf.shift(3)-closePriceDf.shift(2))<(closePriceDf.shift(2)-closePriceDf.shift(1)))
    # 形态5：涨后急涨
    closePriceForm5 = (closePriceDf.shift(1)>closePriceDf.shift(2)) & (closePriceDf.shift(2)>closePriceDf.shift(3)) & ((closePriceDf.shift(1)-closePriceDf.shift(2))>(closePriceDf.shift(2)-closePriceDf.shift(3)))
    # 形态6：涨后缓涨
    closePriceForm6 = (closePriceDf.shift(1)>closePriceDf.shift(2)) & (closePriceDf.shift(2)>closePriceDf.shift(3)) & ((closePriceDf.shift(1)-closePriceDf.shift(2))<(closePriceDf.shift(2)-closePriceDf.shift(3)))
    # 形态7：涨后缓跌
    closePriceForm7 = (closePriceDf.shift(2)>closePriceDf.shift(1)) & (closePriceDf.shift(1)>closePriceDf.shift(3))
    # 形态8：涨后急跌
    closePriceForm8 = (closePriceDf.shift(2)>closePriceDf.shift(3)) & (closePriceDf.shift(3)>closePriceDf.shift(1))
    

    closePriceForm1.to_csv('Data/OperationTable'+calStartDay+'/b-价格1-跌后急涨.csv',encoding='gbk')
    closePriceForm2.to_csv('Data/OperationTable'+calStartDay+'/b-价格2-跌后缓涨.csv',encoding='gbk')
    closePriceForm3.to_csv('Data/OperationTable'+calStartDay+'/b-价格3-跌后缓跌.csv',encoding='gbk')
    closePriceForm4.to_csv('Data/OperationTable'+calStartDay+'/b-价格4-跌后急跌.csv',encoding='gbk')
    closePriceForm5.to_csv('Data/OperationTable'+calStartDay+'/b-价格5-涨后急涨.csv',encoding='gbk')
    closePriceForm6.to_csv('Data/OperationTable'+calStartDay+'/b-价格6-涨后缓涨.csv',encoding='gbk')
    closePriceForm7.to_csv('Data/OperationTable'+calStartDay+'/b-价格7-涨后缓跌.csv',encoding='gbk')
    closePriceForm8.to_csv('Data/OperationTable'+calStartDay+'/b-价格8-涨后急跌.csv',encoding='gbk')

###
# 根据前3月换手率形态，把股票8个换手率形态。股票当月份属于哪个形态，分别用4个布尔CSV保存起来。
###
def genTurnOverFormBoolDf(calStartDay):
    turnOverDf = pd.read_csv('Data/OperationTable'+calStartDay+'/4.turnOverDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    activeDaysDf = pd.read_csv('Data/OperationTable'+calStartDay+'/5.activeDaysDf.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    turnOverDf = turnOverDf.to_period('M')
    activeDaysDf = activeDaysDf.to_period('M')

    turnOverPerDayDf = turnOverDf/activeDaysDf
    # 形态1：跌后急涨
    turnOverForm1 = (turnOverPerDayDf.shift(1)>turnOverPerDayDf.shift(3)) & (turnOverPerDayDf.shift(3)>turnOverPerDayDf.shift(2))
    # 形态2：跌后缓涨
    turnOverForm2 = (turnOverPerDayDf.shift(3)>turnOverPerDayDf.shift(1)) & (turnOverPerDayDf.shift(1)>turnOverPerDayDf.shift(2))
    # 形态3：跌后缓跌
    turnOverForm3 = (turnOverPerDayDf.shift(3)>turnOverPerDayDf.shift(2)) & (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(1)) & ((turnOverPerDayDf.shift(3)-turnOverPerDayDf.shift(2))>(turnOverPerDayDf.shift(2)-turnOverPerDayDf.shift(1)))
    # 形态4：跌后急跌
    turnOverForm4 = (turnOverPerDayDf.shift(3)>turnOverPerDayDf.shift(2)) & (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(1)) & ((turnOverPerDayDf.shift(3)-turnOverPerDayDf.shift(2))<(turnOverPerDayDf.shift(2)-turnOverPerDayDf.shift(1)))
    # 形态5：涨后急涨
    turnOverForm5 = (turnOverPerDayDf.shift(1)>turnOverPerDayDf.shift(2)) & (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(3)) & ((turnOverPerDayDf.shift(1)-turnOverPerDayDf.shift(2))>(turnOverPerDayDf.shift(2)-turnOverPerDayDf.shift(3)))
    # 形态6：涨后缓涨
    turnOverForm6 = (turnOverPerDayDf.shift(1)>turnOverPerDayDf.shift(2)) & (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(3)) & ((turnOverPerDayDf.shift(1)-turnOverPerDayDf.shift(2))<(turnOverPerDayDf.shift(2)-turnOverPerDayDf.shift(3)))
    # 形态7：涨后缓跌
    turnOverForm7 = (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(1)) & (turnOverPerDayDf.shift(1)>turnOverPerDayDf.shift(3))
    # 形态8：涨后急跌
    turnOverForm8 = (turnOverPerDayDf.shift(2)>turnOverPerDayDf.shift(3)) & (turnOverPerDayDf.shift(3)>turnOverPerDayDf.shift(1))
    
    turnOverForm1.to_csv('Data/OperationTable'+calStartDay+'/b-换手1-跌后急涨.csv',encoding='gbk')
    turnOverForm2.to_csv('Data/OperationTable'+calStartDay+'/b-换手2-跌后缓涨.csv',encoding='gbk')
    turnOverForm3.to_csv('Data/OperationTable'+calStartDay+'/b-换手3-跌后缓跌.csv',encoding='gbk')
    turnOverForm4.to_csv('Data/OperationTable'+calStartDay+'/b-换手4-跌后急跌.csv',encoding='gbk')
    turnOverForm5.to_csv('Data/OperationTable'+calStartDay+'/b-换手5-涨后急涨.csv',encoding='gbk')
    turnOverForm6.to_csv('Data/OperationTable'+calStartDay+'/b-换手6-涨后缓涨.csv',encoding='gbk')
    turnOverForm7.to_csv('Data/OperationTable'+calStartDay+'/b-换手7-涨后缓跌.csv',encoding='gbk')
    turnOverForm8.to_csv('Data/OperationTable'+calStartDay+'/b-换手8-涨后急跌.csv',encoding='gbk')