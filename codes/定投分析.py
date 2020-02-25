
# coding: utf-8

# In[ ]:

import datetime
# DataAPI.FundNavGet(dataDate=u"",secID=u"",ticker=u"001021",beginDate=u"20160301",field=u"",pandas="1")
# DataAPI.MktEqudGet(tradeDate=u"",secID=u"510300.XSHG",ticker=u"",beginDate=u"20160101",endDate=u"20160315",field=u"",pandas="1")

DataAPI.MktFunddGet(tradeDate=u"",secID=u"",ticker=u"511010",beginDate=u"",endDate=u"",field=u"",pandas="1")

DataAPI.SecIDGet(partyID=u"",assetClass=u"",ticker=u"513500",cnSpell=u"",field=u"",pandas="1")

# DataAPI.MktEqudGet返回pandas.DataFrame格式的市场日线数据
# MarketEqud =  DataAPI.MktEqudGet(secID = "000002.XSHE", beginDate = "20000106", endDate = "20140110")
#  # 绘制返回的数据
# import seaborn
# MarketEqud.plot(x='tradeDate', y='closePrice',title=u'the Close Price',figsize=(14,6))


# In[ ]:



import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
from dateutil.parser import *
from pandas import DataFrame
import collections

import quartz
from quartz.api import *

import pandas as pd
import numpy as np
# from datetime import datetime
from matplotlib import pylab

tradeDaysDf = DataFrame()
tradeDaysDf = DataAPI.TradeCalGet(exchangeCD=u"XSHG", beginDate=u"", endDate=u"", field=u"", pandas="1")


# tradeDaysDf = tradeDaysDf[tradeDaysDf.isOpen==1]




def get_month_day_range(year, month):
    """
    For a date 'date' returns the start and end date for the month of 'date'.
    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))
    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    date = datetime.date(year, month, 1);
    last_day = date + relativedelta(day=1, months=+1, days=-1)
    first_day = date + relativedelta(day=1)
    return 0, last_day.day


def string_toDatetime(string):
    """把字符串转成datetime"""
    return datetime.datetime.strptime(string, "%Y-%m-%d")


def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")


def add_months(sourcedate, months):
    """某日的下面months个月的那一天"""
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, get_month_day_range(year, month)[1])
    return datetime.datetime(year, month, day)


def nextMonthInvestDay(preInvestDate, intervalMonths, investDay):
    """下个月的定投日"""
    date = add_months(preInvestDate, intervalMonths)
    # 矫正日
    monthdays = get_month_day_range(date.year, date.month)[1]
    date = date.replace(day=min(investDay, monthdays))
    return date


def getDayList(startDate, endDate, investDay):
    """获取日期列表，每个月的investDay天，处理了30，31，28，29日子的问题"""
    #
#     dayList = []
#     startDatetime = string_toDatetime(startDate)
#     endDatetime = string_toDatetime(endDate)
#     # 矫正月份
#     firstInvestDatetime = startDatetime;
#     firstInvestDatetime = datetime.datetime(startDatetime.year, startDatetime.month,
#                                             startDatetime.day) if startDatetime.day <= investDay \
#         else add_months(startDatetime, 1)
#     # 矫正日
#     monthdays = get_month_day_range(firstInvestDatetime.year, firstInvestDatetime.month)[1]
#     firstInvestDatetime = firstInvestDatetime.replace(day=min(investDay, monthdays))

#     # investPool.setdefault(firstInvestDatetime, True)
#     tmpData = firstInvestDatetime;
#     while (tmpData <= endDatetime):
#         dayList.append(tmpData)
#         tmpData = nextMonthInvestDay(tmpData, 1, investDay)

    # 这种方式更优雅 MONTHLY-每月, bymonthday -1 每月的最后一天, dtstart起始日期,until结束日期
    dayList = list(rrule(MONTHLY, bymonthday=investDay, bysetpos=1, dtstart=parse(startDate), until=parse(endDate)))
    return dayList


def isTradeOpen(date):
    """是否是开盘日"""
    dateString = datetime_toString(date)
    tmp = tradeDaysDf[tradeDaysDf.calendarDate == dateString]
    if tmp.empty:
        return False
    else:
        return tmp.iloc[0].isOpen


def getFollowTradeDate(investDate, position = 1):
    """获取下一个可以交易的日期"""
    result = None
    index = 0
    for i in range(10+position+position/7*2):
        ## 策略：从invest到invest+9找交易日
        date = investDate + relativedelta(days=+i)
        if isTradeOpen(date):
            index=index+1
            if position==index:
                result = date
                break;
    return result


def getPreTradeDate(investDate,position = 1):
    """获取之前可以交易的日期"""
    result = None
    index = 0
    for i in range(10+position+position/7*2):
        ## 策略：从invest到invest+9找交易日
        date = investDate + relativedelta(days=-i)
        if isTradeOpen(date): 
            index = index+1
            if position==index:
                result = date
                break;
    return result


def getFixedInvestTradeDays(startDate, endDate, investDay):
    """获取定投交易日的列表，返回OrderedDict顺序字典"""
    dayList = getDayList(startDate, endDate, investDay)  # 获取日期列表
    tradePool = collections.OrderedDict()  # 交易日期池
    startDatetime = string_toDatetime(startDate)
    endDatetime = string_toDatetime(endDate)
    # 对每个日期矫正到交易日
    for day in dayList:
        # 可能会有空的清空，很少见
        tradedate = getFollowTradeDate(day)
        if tradedate != None:
            tradePool[tradedate] = True
        else:
            tradePool[day] = False
        pass
    return tradePool


def getFixedInvestBalanceDays(startDate, endDate,balanceMonth):
    """获取定投重新平衡日的列表，返回OrderedDict顺序字典"""
    balancePool = collections.OrderedDict()  # 平衡日期池
    # 默认每年的最后一天平衡
    dayList =list(rrule(MONTHLY, bymonth=balanceMonth,bymonthday=(-1,), bysetpos=1, dtstart=parse(startDate), until=parse(endDate)))
    # dayList = list(rrule(YEARLY, byyearday=(-1,), bysetpos=1, dtstart=parse(startDate), until=parse(endDate)))
    for day in dayList:
        tradedate = getPreTradeDate(day)
        if tradedate != None:
            balancePool[tradedate] = True
        else:
            balancePool[day] = False
        pass
    print
    return balancePool




start = '2015-06-1'                       # 回测起始时间
end = '2016-03-18'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
universe = ['510300.XSHG','510050.XSHG','513100.XSHG','001021.XSHG']  # 证券池，支持股票和基金'510050.XSHG'
dingtou_monthly=100000
weight = [1,1,1,1]
capital_base = 10000000                      # 起始资金
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                          # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

rebalance_flag=True
dingtou_day=(15,) #定投日，每月的-1最后一天
rebalance_month=(6,12) # 平衡月，1月的最后一天
def initialize(account):                   # 初始化虚拟账户状态
    account.fixedInvestDays = getFixedInvestTradeDays(start, end, dingtou_day)
    
    # print account.fixedInvestDays
    account.fixedInvestBalanceDays = getFixedInvestBalanceDays(start, end,rebalance_month)
    # print account.fixedInvestBalanceDays
    account.weight = weight
    account.weightmap = dict(zip(universe, account.weight))
    # w = account.weightmap.get(stock, 0)
    account.test = True
    account.dingtou_sum_monthly=dingtou_monthly
    account.weightdingtou=dict(zip(universe, np.array(account.weight)/float(sum(account.weight))*account.dingtou_sum_monthly))
    print account.weightdingtou
    account.dingtou_cash =0
    account.dingtou_his ={}
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    # print str(account.current_minute)
    # # if account.current_minute=='14:50' and account.test:
    #     order('510300.XSHG', 100)
    #     account.test = False
    account.dingtou_his[account.current_date]=account.dingtou_cash
    isBalanceDay = False    
    try:
        isBalanceDay = account.fixedInvestBalanceDays[account.current_date]
    except:
        pass
        # print str(account.current_date) + "not  balance day"
        
    if isBalanceDay:
        if not rebalance_flag:
            return
        # print log.info("is balance day!!!!!!!!")
        sum_value = account.referencePortfolioValue-(capital_base-account.dingtou_cash)#account.cash

        # for stk in account.universe:  
        #     sum +=account.valid_secpos[stk]*account.referencePrice[stk]
        
    
        averge=dict(zip(universe, np.array(account.weight)/float(sum(account.weight))*sum_value))                
        print averge
        longstr=""
        for stk in account.universe:  
            order_to(stk, averge[stk]//account.referencePrice[stk])
            # print str(stk)+": "+str(account.valid_secpos[stk]*account.referencePrice[stk])+" -> "+str(averge[stk])+" "+str(account.referencePrice[stk])
            # print log.info("balance " + stk+" order_to: "+str(averge[stk]))
        pass
        log.info("balance: " +str(account.valid_secpos))
        return ##  平衡日与定投日冲突的情况
        
    ####
    isInvestDay = False
    try:
        isInvestDay = account.fixedInvestDays[account.current_date]
    except:
        pass
        # print str(account.current_date) + "not invetday"
    
    if isInvestDay:
        # print str(account.current_date) + "is invetday!!!!!!!!"
        # hist = account.get_attribute_history('closePrice', 10)
        for stk in account.universe:  
            print stk+" order:"+str(account.weightdingtou[stk])+" "+str(account.referencePrice)
            # print str(2000//account.referencePrice[stk])
            order(stk, account.weightdingtou[stk]//account.referencePrice[stk])
            account.dingtou_cash+=account.weightdingtou[stk]
        # 重设定投数据
        account.dingtou_his[account.current_date]=account.dingtou_cash
        log.info( account.valid_secpos)
        pass

    
    return


def recalculate(bt):
    newdf= pd.DataFrame()
    # newdf['tradeDate']=bt.tradeDate
    # 投资成本，实际投资的钱 == 初始现金 - 账户剩余现金
    newdf['cost']=capital_base-bt.cash
    # 股票价格 == 总的账户价格（现金+股票）- 账户剩余现金
    newdf['position_value']=bt.portfolio_value-bt.cash

    newdf.index=bt.tradeDate # 设置日期为索引
    newdf['dingtou_cash']=pd.Series(acct.dingtou_his)
    return newdf


# bt, acct = quartz.backtest(start = start,end = end,benchmark = benchmark,\
#                             universe = universe,\
#              capital_base = capital_base,\
#              initialize = initialize,\
#              handle_data = handle_data,\
#              refresh_rate = refresh_rate)
# perf = quartz.perf_parse(bt, acct)

# out_keys = ['annualized_return', 'volatility', 'information_ratio', 'sharpe', 'max_drawdown', 'alpha', 'beta']
# for k in out_keys:
#      print '%s:%s' % (k, perf[k])
# perf['cumulative_returns'].plot()

# position_value=bt.portfolio_value-bt.cash
# print capital_base -acct.cash,acct.dingtou_cash

# newdf = recalculate(bt)
# ((newdf['position_value']-newdf['cost'])/newdf['cost']).plot()
# print newdf

rebalance_flag=True
    
for i in (0,1,2,3,4,5,6):
    # dingtou_day=(i,)
    if i==0:
        universe = ['510300.XSHG'] ##163210
        weight = [1]
        rebalance_month=[12]
    if i==1:
        universe = ['513100.XSHG'] ##163210
        weight = [1]
        rebalance_month=[12]
    if i==2:
        universe = ['163210.XSHE'] ##163210
        weight = [1]
        rebalance_month=[12]
    if i==3:
        universe = ['511880.XSHG'] ##163210
        weight = [1]
        rebalance_month=[12]
    if i==4:
        universe = ['510300.XSHG','510500.XSHG','513100.XSHG','513500.XSHG','163210.XSHE'] # 极简理财方案，波动小一些，美股因素较大
        weight = [1,1,1,1,1]
        rebalance_month=[4,8,12]
    if i==5:
        universe = ['510300.XSHG','510500.XSHG','513100.XSHG','163210.XSHE'] ##163210
        weight = [1,1,1,1]
        rebalance_month=[4,8,12]
    if i==6:
        universe = ['510300.XSHG','510500.XSHG','513100.XSHG','163210.XSHE'] ## 波动最小，比较保守
        weight = [1,1,1,2]
        rebalance_month=[4,8,12]
        
   
    # 生成month
    # rebalance_month=[]
    # step=12//(i+1)
    # month_tmp=0
    # for j in range(i+1):
    #     month_tmp+=step
    #     rebalance_month.append(month_tmp)
    
    bt, acct = quartz.backtest(start = start,end = end,benchmark = benchmark,                            universe = universe,             capital_base = capital_base,             initialize = initialize,             handle_data = handle_data,             refresh_rate = refresh_rate)
    newdf = recalculate(bt)
    ((newdf['position_value']-newdf['cost'])/newdf['cost']).plot(figsize=(20,6))
    # print newdf

# newdf['cost'].plot()
# newdf['position_value'].plot()

# newdf['dingtou_cash'].plot()

# perf['benchmark_cumulative_returns'].plot()
pylab.legend(['A', 'usa','bond','Monetary fund','jijian','1:1:1:1','1:1:1:2'])


# In[ ]:




# In[ ]:




# In[ ]:



