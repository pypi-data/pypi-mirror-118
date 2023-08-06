# -*- coding: utf-8 -*-


import os; os.chdir("S:/siateng")
from siate import *
#==============================================================================

Market={'Market':('China','000001.SS')}
Stocks={'600519.SS':0.25,'000858.SZ':0.25,'000596.SZ':0.25,'600779.SS':0.25}
portfolio=dict(Market,**Stocks)
pf_info=portfolio_cumret(portfolio,'2021-7-7',pastyears=1)
es_info=portfolio_es(pf_info,simulation=50000)
df=portfolio_MSR_GMV(es_info)

#==============================================================================
stock_share,df0=es_info
df=df0.copy()

import math
decimals=2
keep2decimals=lambda x: math.floor(x*10**decimals)/(10**decimals)
#df['Volatility2']=round(df['Volatility'],2)
df['Volatility2']=df['Volatility'].apply(keep2decimals)

df_max=df.groupby('Volatility2').agg({'Returns':max})
plt.plot(df_max.index,df_max['Returns'],color='g',ls=':',lw=1)

df_min=df.groupby('Volatility2').agg({'Returns':min})
plt.plot(df_min.index,df_min['Returns'],color='r',ls=':',lw=1)

plt.xlabel=''
plt.ylabel=''
plt.show()

#==============================================================================

portfolio_corr(pf_info)

translate_tickerlist(Stocks)
#==============================================================================
stocks=['600519.SS','000858.SZ','000596.SZ','600779.SS','603589.SS','000568.SZ','000799.SZ','600809.SS']
fromdate='2020-7-7'
todate='2021-7-7'
ef=portfolio_ef(stocks,fromdate,todate)
#==============================================================================




#==============================================================================
Market={'Market':('US','^GSPC')}
Stocks={'AAPL':.1,'MSFT':.13,'XOM':.09,'JNJ':.09,'JPM':.09,'AMZN':.15,'GE':.08,'FB':.13,'T':.14}
portfolio=dict(Market,**Stocks)

pf_info=portfolio_cumret(portfolio,'2019-12-31')
portfolio_covar(pf_info)
portfolio_corr(pf_info)
portfolio_expectation(pf_info)

es_info=portfolio_es(pf_info,simulation=50000)

df=portfolio_MSR_GMV(es_info)

stocks=['IBM','WMT','AAPL','C','MSFT']
ef=portfolio_ef(stocks,'2019-1-1','2020-8-1')





_,_,tickerlist,sharelist=decompose_portfolio(portfolio)

today='2020-12-31'
pastyears=1

pf_info=portfolio_cumret(portfolio,'2020-12-31')

portfolio_covar(pf_info)

portfolio_corr(pf_info)


















#定义投资组合
Market={'Market':('US','^GSPC')}
Stocks={'BABA':.4,'JD':.3,'PDD':.2,'VIPS':.1}
portfolio=dict(Market,**Stocks)

#搜寻该投资组合中所有成分股的价格信息，默认观察期为一年，pastyears=1
pf_info=portfolio_cumret(portfolio,'2020-11-30',pastyears=1)

#生成了投资组合的可行集
es_info=portfolio_es(pf_info,simulation=50000)
es_info10=portfolio_es(pf_info,simulation=100000)

#寻找投资组合的MSR优化策略点和GMV优化策略点
psr=portfolio_MSR_GMV(es_info)
