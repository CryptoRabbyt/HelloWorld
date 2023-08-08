# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import urllib.request
import re
import time
import os
import datetime


# %%
if (os.path.exists(".\\Data\\StockData")):
    os.rename(".\\Data\\StockData",".\\Data\\StockData-"+datetime.datetime.now().strftime('%Y-%m-%d'))
    print("StockData-"+datetime.datetime.now().strftime('%Y-%m-%d'))
if (os.path.exists(".\\Data\\OperationTable20050401")):
    os.rename(".\\Data\\OperationTable20050401",".\\Data\\OperationTable20050401-"+datetime.datetime.now().strftime('%Y-%m-%d'))
    print("OperationTable20050401-"+datetime.datetime.now().strftime('%Y-%m-%d'))
os.makedirs(".\\Data\\StockData")
os.makedirs(".\\Data\\OperationTable20050401")


# %%
def urlTolist(url):
    allCodeList = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    print(html)

    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)

    for item in code:
        print(item)
        if item[0]=='6' or item[0]=='3' or item[0]=='0':
            allCodeList.append(item)
    return allCodeList


# %%
stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
allCodelist = urlTolist(stock_CodeUrl)
allCodelist

# %% [markdown]
# 获取全股票代码

# %%
n = 1
codeList = list()
while(True):
    if(n%10==0):
        print(n)
    #中小板
    #url = "http://88.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240365865449866579_1586191680279&pn="+str(n)+"&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:13&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1586191680280"
    #A股
    url = "http://95.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240818354900041369_1586193567961&pn="+str(n)+"&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1586193567962"
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')

    s = r'"f12":"(\d*?)"'
    pat = re.compile(s)
    code = pat.findall(html)
    if(len(code)<=0):
        break
    else:
        codeList.extend(code)
        n=n+1
codeList[:6]

# %% [markdown]
# if(not os.path.exists('Data/OperationTable'+calStartDay)):
#     os.makedirs('Data/OperationTable'+calStartDay)

# %%
n=1
for code in codeList:
    print('正在获取%s股票数据...'%code)
    print(n)
    n+=1
    if code[0]=='6':
        url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+        '&end=20801231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    else:
        url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code+        '&end=20801231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    try:
        urllib.request.urlretrieve(url,'d:\\ThinkingData\\Data\\StockData\\'+code+'.csv')#可以加一个参数dowmback显示下载进度
    except Exception as e:
        print (Exception,":",e)
        
    time.sleep(0.5)

# %% [markdown]
# 需要分析的数据是从什么时候开始的！

# %%
calStartDay = '20050401'


# %%
import AggStockData

path = 'Data/StockData/'
# calStartDay = '20050401'
reserveDataMonths = 24
AggStockData.aggDatas(path,calStartDay,reserveDataMonths)


# %%
import GenerateBoolDf

# calStartDay = '20050401'
GenerateBoolDf.genIsMacdRiseCsv(calStartDay)
GenerateBoolDf.genIsMacdFallCsv(calStartDay)
GenerateBoolDf.genIsMacdTrendUp(calStartDay)
GenerateBoolDf.genMacdSpreadDf(calStartDay)
GenerateBoolDf.genIsMacdRiseAndFallCsv(calStartDay)
GenerateBoolDf.genIsMacdFallAndRiseCsv(calStartDay)
# GenerateBoolDf.genIsMacdEqu(calStartDay)
# GenerateBoolDf.genIsTurnOverRise(calStartDay)
# GenerateBoolDf.genIsTurnOverBetween(calStartDay,0.5,3,24)
# GenerateBoolDf.genIsMarketValueBetween(calStartDay,2000000000,10000000000)
# GenerateBoolDf.genTrendSpreadDf(calStartDay,[0.4,1.5,5,0.5])
GenerateBoolDf.genIsMonthPass(calStartDay)
# GenerateBoolDf.genIsMarketValueGt(calStartDay,1000000000)
# GenerateBoolDf.genMarketValueRange(calStartDay)
GenerateBoolDf.genTrendBoolDf(calStartDay)
GenerateBoolDf.genTrendSpreadDf(calStartDay,[1,5,2,1])
# GenerateBoolDf.genPriceFormBoolDf(calStartDay)
GenerateBoolDf.genTurnOverFormBoolDf(calStartDay)
GenerateBoolDf.genTurnOverPerDayRange(calStartDay)


# %%



