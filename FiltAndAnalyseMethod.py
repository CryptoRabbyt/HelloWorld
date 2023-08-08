import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

###
# 读取CSV，并把Index转换为“月”周期
###
def readCsv(calStartDay,fileName):
    df = pd.read_csv('Data/OperationTable'+calStartDay+'/'+fileName+'.csv',index_col=0,parse_dates=[0],encoding='gbk',memory_map=True)
    df = df.to_period('M')
    df.name = fileName
    return df

###
# 筛选后的rateDf计算平均涨幅，可选数量，涨幅累积，并保存到CSV
###
def toCsv(calStartDay,df,fileName):
    df['mean'] = df.mean(axis=1)
    df['mean'] = df['mean'].fillna(1)
    df['count'] = df.count(axis=1)-1
    df['cumprod'] = df['mean'].cumprod()

    df.to_csv('Data/OperationTable'+calStartDay+'/'+fileName+'.csv',encoding='gbk')
    return df

### 弃用
# 输入正向Df和反向Df，返回一个Series，保存在每一行中，正向Df的True数量与反向DF的差值，占两个DF True总数的百分比，从而反映市场趋势
###
def getTrendDf(forwardDf,oppositeDf):
    forwardCount = forwardDf.apply(lambda x:x[x==True].count(),axis = 1)
    oppositeCount = oppositeDf.apply(lambda x:x[x==True].count(),axis = 1)
    return (forwardCount-oppositeCount)/(forwardCount+oppositeCount)

### 弃用
# 先根据条件筛选出需要操作的月份，并按照布尔DF把不为TRUE的数据点设为np.nan
# df：过滤前的DataFrame
# operationSer：标记哪一个月需要进行操作的布尔Series
# boolDf：标记哪一个点为及格数据点的布尔DataFrame
###
def flitDfByCondition(df,operationSer,boolDf):
    boolDfCopy = boolDf.copy()
    boolDfCopy[~operationSer] = True
    df = df[boolDfCopy]
    return df

###
# 判断目标条件在指定趋势的情况下的表现
# result4ConsDf：保存了不同条件在不同SAR趋势情况下的表现
# rateDf：初步过滤后的涨幅DF
# sarFormPerMonthSer：各个月份SAR趋势是否为指定趋势的布尔Series
# sarFormId：要判断的Sar趋势
# conDf_A：条件的布尔DF
# conName：条件类型名称
###
def appendConsResult(calStartDay,result4ConsDf,rateDf,sarFormPerMonthSer,sarFormId,conDf_A,conName):
    rateDfTrend = rateDf[sarFormPerMonthSer]
    trendMonthCount = rateDfTrend.shape[0]

    # 在趋势月份，应用条件布尔DF后的涨幅DF
    rateDfAfterFilt = rateDf[sarFormPerMonthSer]
    rateDfAfterFilt = rateDfAfterFilt[conDf_A]

    rateDfAfterFilt_Count = rateDfAfterFilt.count(axis=1)

    rateDfTrend = rateDfTrend[rateDfAfterFilt_Count>0]
    rateDfAfterFilt = rateDfAfterFilt[rateDfAfterFilt_Count>0]
    gt0MonthCount = rateDfTrend.shape[0]

    rateDfTrend_10 = rateDfTrend[rateDfAfterFilt_Count>20]
    # rateDfAfterFilt_10 = rateDfAfterFilt[rateDfAfterFilt_Count>20]
    gt10MonthCount = rateDfTrend_10.shape[0]

    if(conName=='市值'):
        ratePerWeightedAver = calcRatePerWeightedAver(rateDfAfterFilt,pd.Timestamp.now()-96*MonthEnd(),96,rateDf)
    else:
        ratePerWeightedAver = calcRatePerWeightedAver(rateDfAfterFilt,calStartDay,calcMonthFromSerName(rateDf[calStartDay:].iloc[0])*0.7,rateDf)

    resultIndex = pd.MultiIndex.from_arrays([[str(sarFormId)],[conName],[conDf_A.name]])
    resultDf = pd.DataFrame({#'平均涨幅':rateDfAfterFilt.mean(axis=1).mean(),
                            # '涨幅比':rateDfAfterFilt.mean(axis=1).mean()/rateDfTrend.mean(axis=1).mean(),
                            # '平均涨幅(>20人':rateDfAfterFilt_10.mean(axis=1).mean(),
                            # '涨幅比(>20人':rateDfAfterFilt_10.mean(axis=1).mean()/rateDfTrend_10.mean(axis=1).mean(),
                            '平均数量':rateDfAfterFilt_Count.mean(),
                            '样本月份':trendMonthCount,
                            '样本数量':rateDfAfterFilt_Count.sum(),
                            '非0率':gt0MonthCount/trendMonthCount,
                            '人多率':gt10MonthCount/trendMonthCount,
                            # '人多样本':gt10MonthCount,
                            '加权平均涨幅比':ratePerWeightedAver
                            },index=resultIndex)#+'<>'+conDf_C.name
    
    return result4ConsDf.append(resultDf)

def calcMonthFromSerName(x):
    if((pd.Period.now(freq="M") - x.name).freqstr[:-1]==""):
        return 1
    else:
        return int((pd.Period.now(freq="M") - x.name).freqstr[:-1])

###
# 传入：rateDfAfterFlit： 应用条件筛选后的DF
# 起始纳入计算的日期
# 起始日期的权重（每后移1个月，权重加1）
# 返回：加权平均涨幅
###
# def calcRateWeightedAver(rateDfAfterFlit,calStartDay,weightOfBegin):
#     rateDfAfterFlit = rateDfAfterFlit[calStartDay:]

#     # 权重Series
#     weightSer = rateDfAfterFlit.apply(calcMonthFromSerName,axis=1)
#     weightSer = weightSer[0] - weightSer + weightOfBegin

#     # 涨幅总和Ser
#     rateSumSer = rateDfAfterFlit.sum(axis=1)

#     # 样本总和Ser
#     rateCountSer = rateDfAfterFlit.count(axis=1)

#     # 加权平均涨幅 = (涨幅总和Ser * 权重Ser).sum() / (总数Ser * 权重Ser).sum()
#     return (rateSumSer*weightSer).sum()/(rateCountSer*weightSer).sum()

###
# 传入：rateDfAfterFlit： 应用条件筛选后的DF
# 起始纳入计算的日期
# 起始日期的权重（每后移1个月，权重加1）
# 未过滤的涨幅DF
# 返回：加权平均涨幅
###
def calcRatePerWeightedAver(rateDfAfterFlit,calStartDay,weightOfBegin,rateDf):
    rateDfAfterFlit = rateDfAfterFlit[calStartDay:]
    if(rateDfAfterFlit.empty):
        return 0
    # 权重Series
    weightSer = rateDfAfterFlit.apply(calcMonthFromSerName,axis=1)
    weightSer = weightSer[0] - weightSer + weightOfBegin

    # 将涨幅转化为涨幅比
    rateDfAfterFlit = rateDfAfterFlit.div(rateDf.mean(axis=1),axis=0)

    # 涨幅总和Ser
    rateSumSer = rateDfAfterFlit.sum(axis=1)

    # 样本总和Ser
    rateCountSer = rateDfAfterFlit.count(axis=1)

    print((rateSumSer*weightSer).sum()/(rateCountSer*weightSer).sum())
    # 加权平均涨幅 = (涨幅总和Ser * 权重Ser).sum() / (总数Ser * 权重Ser).sum()
    return (rateSumSer*weightSer).sum()/(rateCountSer*weightSer).sum()


###
# 传入：趋势编号
# 传入：条件类型
# 返回：列表

def getTop2ConList(result4ConsDf,sarFormId,conName):
    top2ConList = result4ConsDf.loc[sarFormId,conName].sort_values(by=['加权平均涨幅比'],ascending=False)
    top2ConList = ((top2ConList['样本数量']>1000)&(top2ConList['加权平均涨幅比']>1))[:3]
    if(len(top2ConList)==0):
        top2ConList = result4ConsDf.loc[sarFormId,'价格'].sort_values(by=['加权平均涨幅比'],ascending=False)[:1]
    return top2ConList.index.values

###
# 判断目标条件在指定趋势的情况下的表现
# result4ConsDf：保存了不同条件在不同SAR趋势情况下的表现
# rateDf：初步过滤后的涨幅DF
# sarFormPerMonthSer：各个月份SAR趋势是否为指定趋势的布尔Series
# sarFormId：要判断的Sar趋势
# conDf_A：条件的布尔DF
# conName：条件类型名称
###
def appendConsResult_3Con(calStartDay,result4ConsDf,rateDf,sarFormPerMonthSer,sarFormId,conDf_A,conDf_B,conDf_C):
    rateDfTrend = rateDf[sarFormPerMonthSer]
    trendMonthCount = rateDfTrend.shape[0]

    rateDfAfterFilt = rateDf[sarFormPerMonthSer]
    rateDfAfterFilt = rateDfAfterFilt[conDf_A][conDf_B][conDf_C]

    rateDfAfterFilt_Count = rateDfAfterFilt.count(axis=1)

    rateDfTrend = rateDfTrend[rateDfAfterFilt_Count>0]
    rateDfAfterFilt = rateDfAfterFilt[rateDfAfterFilt_Count>0]
    gt0MonthCount = rateDfTrend.shape[0]

    rateDfTrend_10 = rateDfTrend[rateDfAfterFilt_Count>10]
    # rateDfAfterFilt_10 = rateDfAfterFilt[rateDfAfterFilt_Count>10]
    gt10MonthCount = rateDfTrend_10.shape[0]

    ratePerWeightedAver = calcRatePerWeightedAver(rateDfAfterFilt,calStartDay,calcMonthFromSerName(rateDf[calStartDay:].iloc[0])*0.7,rateDf)
        
    resultIndex = pd.MultiIndex.from_arrays([[str(sarFormId)],[conDf_A.name],[conDf_B.name],[conDf_C.name]])
    resultDf = pd.DataFrame({'平均涨幅':rateDfAfterFilt.mean(axis=1).mean(),
                            # '涨幅比':rateDfAfterFilt.mean(axis=1).mean()/rateDfTrend.mean(axis=1).mean(),
                            # '平均涨幅(>10人':rateDfAfterFilt_10.mean(axis=1).mean(),
                            # '涨幅比(>10人':rateDfAfterFilt_10.mean(axis=1).mean()/rateDfTrend_10.mean(axis=1).mean(),
                            '平均数量':rateDfAfterFilt_Count.mean(),
                            '样本月份':trendMonthCount,
                            '样本数量':rateDfAfterFilt_Count.sum(),
                            '非0率':gt0MonthCount/trendMonthCount,
                            '人多率':gt10MonthCount/trendMonthCount,
                            # '人多样本':gt10MonthCount,
                            '加权平均涨幅比':ratePerWeightedAver
                            },index=resultIndex)#+'<>'+conDf_C.name
    
    return result4ConsDf.append(resultDf)


def testDays(df,testLastDay):
    reDf = df[:testLastDay]
    print(df.name)
    reDf.name = df.name
    print(reDf.name)
    return reDf