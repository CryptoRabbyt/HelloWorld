# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import FiltAndAnalyseMethod as fam


# %%
calStartDay = '20050401'
# testLastDay = '20200301'


isMacdRiseDf = fam.readCsv(calStartDay,'b-MACD连涨')
isMacdFallDf = fam.readCsv(calStartDay,'b-MACD连跌')
isMacdF2RDf = fam.readCsv(calStartDay,'b-MACD转升')
isMacdR2FDf = fam.readCsv(calStartDay,'b-MACD转跌')
isMacdTrendUp = fam.readCsv(calStartDay,'b-MACD趋势上升')
macdSpreadDf = fam.readCsv(calStartDay,'b-macd趋势分布')

priceRiseFormDf = fam.readCsv(calStartDay,'b-sar上涨形成趋势')
priceRiseStagnateDf = fam.readCsv(calStartDay,'b-sar上涨停滞趋势')#有用
priceFallFormDf = fam.readCsv(calStartDay,'b-sar下跌形成趋势')
priceFallStagnateDf = fam.readCsv(calStartDay,'b-sar下跌停滞趋势')
trendSpreadDf = fam.readCsv(calStartDay,'b-sar趋势分布')

turnOverPerDayRangeDf = fam.readCsv(calStartDay,'type-平均每日换手所属区间')

# marketValueRangeDf = fam.readCsv(calStartDay,'type-市值所属区间')
# marketValueRange1 = (marketValueRangeDf==0)#[:testLastDay]
# marketValueRange2 = (marketValueRangeDf==1)#[:testLastDay]
# marketValueRange3 = (marketValueRangeDf==2)#[:testLastDay]
# marketValueRange4 = (marketValueRangeDf==3)#[:testLastDay]
# marketValueRange5 = (marketValueRangeDf==4)#[:testLastDay]
# marketValueRange6 = (marketValueRangeDf==5)#[:testLastDay]
# marketValueRange7 = (marketValueRangeDf==6)#[:testLastDay]
# marketValueRange8 = (marketValueRangeDf==7)#[:testLastDay]

# marketValueRange1.name = '市值所属区间1'
# marketValueRange2.name = '市值所属区间2'
# marketValueRange3.name = '市值所属区间3'
# marketValueRange4.name = '市值所属区间4'
# marketValueRange5.name = '市值所属区间5'
# marketValueRange6.name = '市值所属区间6'
# marketValueRange7.name = '市值所属区间7'
# marketValueRange8.name = '市值所属区间8'
# marketValueRanges = {'市值所属区间1':marketValueRange1,'市值所属区间2':marketValueRange2,
#                     '市值所属区间3':marketValueRange3,'市值所属区间4':marketValueRange4,
#                     '市值所属区间5':marketValueRange5,'市值所属区间6':marketValueRange6,
#                     '市值所属区间7':marketValueRange7,'市值所属区间8':marketValueRange8}

# closePriceForm1 = fam.readCsv(calStartDay,'b-价格1-跌后急涨')
# closePriceForm2 = fam.readCsv(calStartDay,'b-价格2-跌后缓涨')
# closePriceForm3 = fam.readCsv(calStartDay,'b-价格3-跌后缓跌')
# closePriceForm4 = fam.readCsv(calStartDay,'b-价格4-跌后急跌')
# closePriceForm5 = fam.readCsv(calStartDay,'b-价格5-涨后急涨')
# closePriceForm6 = fam.readCsv(calStartDay,'b-价格6-涨后缓涨')
# closePriceForm7 = fam.readCsv(calStartDay,'b-价格7-涨后缓跌')
# closePriceForm8 = fam.readCsv(calStartDay,'b-价格8-涨后急跌')
# closePriceForms = {'b-价格1-跌后急涨':closePriceForm1,'b-价格2-跌后缓涨':closePriceForm2,
#                 'b-价格3-跌后缓跌':closePriceForm3,'b-价格4-跌后急跌':closePriceForm4,
#                 'b-价格5-涨后急涨':closePriceForm5,'b-价格6-涨后缓涨':closePriceForm6,
#                 'b-价格7-涨后缓跌':closePriceForm7,'b-价格8-涨后急跌':closePriceForm8}

turnOverForm1 = fam.readCsv(calStartDay,'b-换手1-跌后急涨')
turnOverForm2 = fam.readCsv(calStartDay,'b-换手2-跌后缓涨')
turnOverForm3 = fam.readCsv(calStartDay,'b-换手3-跌后缓跌')
turnOverForm4 = fam.readCsv(calStartDay,'b-换手4-跌后急跌')
turnOverForm5 = fam.readCsv(calStartDay,'b-换手5-涨后急涨')
turnOverForm6 = fam.readCsv(calStartDay,'b-换手6-涨后缓涨')
turnOverForm7 = fam.readCsv(calStartDay,'b-换手7-涨后缓跌')
turnOverForm8 = fam.readCsv(calStartDay,'b-换手8-涨后急跌')
turnOverForms = {'b-换手1-跌后急涨':turnOverForm1,'b-换手2-跌后缓涨':turnOverForm2,
                'b-换手3-跌后缓跌':turnOverForm3,'b-换手4-跌后急跌':turnOverForm4,
                'b-换手5-涨后急涨':turnOverForm5,'b-换手6-涨后缓涨':turnOverForm6,
                'b-换手7-涨后缓跌':turnOverForm7,'b-换手8-涨后急跌':turnOverForm8}

# marketValueRange1 = fam.testDays(marketValueRange1,testLastDay)
# marketValueRange2 = fam.testDays(marketValueRange2,testLastDay)
# marketValueRange3 = fam.testDays(marketValueRange3,testLastDay)
# marketValueRange4 = fam.testDays(marketValueRange4,testLastDay)
# marketValueRange5 = fam.testDays(marketValueRange5,testLastDay)
# marketValueRange6 = fam.testDays(marketValueRange6,testLastDay)
# marketValueRange7 = fam.testDays(marketValueRange7,testLastDay)
# marketValueRange8 = fam.testDays(marketValueRange8,testLastDay)

# closePriceForm1 = fam.testDays(closePriceForm1,testLastDay)
# closePriceForm2 = fam.testDays(closePriceForm2,testLastDay)
# closePriceForm3 = fam.testDays(closePriceForm3,testLastDay)
# closePriceForm4 = fam.testDays(closePriceForm4,testLastDay)
# closePriceForm5 = fam.testDays(closePriceForm5,testLastDay)
# closePriceForm6 = fam.testDays(closePriceForm6,testLastDay)
# closePriceForm7 = fam.testDays(closePriceForm7,testLastDay)
# closePriceForm8 = fam.testDays(closePriceForm8,testLastDay)

# turnOverForm1 = fam.testDays(turnOverForm1,testLastDay)
# turnOverForm2 = fam.testDays(turnOverForm2,testLastDay)
# turnOverForm3 = fam.testDays(turnOverForm3,testLastDay)
# turnOverForm4 = fam.testDays(turnOverForm4,testLastDay)
# turnOverForm5 = fam.testDays(turnOverForm5,testLastDay)
# turnOverForm6 = fam.testDays(turnOverForm6,testLastDay)
# turnOverForm7 = fam.testDays(turnOverForm7,testLastDay)
# turnOverForm8 = fam.testDays(turnOverForm8,testLastDay)


# %%
# priceRiseFormDf[~(trendSpreadDf['趋势类型']==0)]=True#//
priceRiseStagnateDf[~(trendSpreadDf['趋势类型(加权']==1)]=True
priceFallFormDf[~(trendSpreadDf['趋势类型(加权']==2)]=True
# priceFallStagnateDf[~(trendSpreadDf['趋势类型']==3)]=True#//

isTurnOverDown = turnOverForm3|turnOverForm4#|turnOverForm7|turnOverForm8


# %%
tex = 0.003#手续费
rateDf = fam.readCsv(calStartDay,'2.rateDf')-tex
rateDf[rateDf>2] = 1
# rateDf = rateDf[:testLastDay]
rateDf.iloc[-1] = 1

print(rateDf[calStartDay:].mean(axis=1).cumprod())

rateDf = rateDf[priceRiseStagnateDf]                [priceFallFormDf]                [isTurnOverDown]
rateDf[macdSpreadDf['趋势类型']==0] = np.nan
rateDf[macdSpreadDf['趋势类型']==4] = np.nan #---------------下降遇两连4，第2个月4也可以买！！！

print(rateDf[calStartDay:].mean(axis=1).cumprod())

rateDf = rateDf[(turnOverPerDayRangeDf==1)|                (turnOverPerDayRangeDf==2)|                (turnOverPerDayRangeDf==3)]
# rateDf = rateDf[(turnOverPerDayRangeDf==2)]#-------------减少筛选项（重要）-------------------------------------

print(rateDf[calStartDay:].mean(axis=1).cumprod())

###########
rateDf['mean'] = rateDf.mean(axis=1)
rateDf['mean'] = rateDf['mean'].fillna(1)
rateDf['count'] = rateDf.count(axis=1)-1
rateDf['cumprod'] = rateDf['mean'].cumprod()
rateDf['趋势类型:数值越大上涨越多'] = macdSpreadDf['趋势类型']

rateDf.to_csv('Data/OperationTable'+calStartDay+'/r-筛选后涨幅CSV.csv',encoding='gbk')
#############


