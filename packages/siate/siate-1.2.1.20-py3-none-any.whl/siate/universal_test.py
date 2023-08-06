# -*- coding: utf-8 -*-


#======================================================================
import os;os.chdir("/Volumes/MAXELL57/siateng")

import os;os.chdir("S:/siateng")
from siate import *
compare_security(['^VIX','^GSPC'],'Close','2011-1-1','2020-12-31',twinx=True)

tickers=['601398.SS','601939.SS','601288.SS','601988.SS','601328.SS','600036.SS','601658.SS']
institution=compare_snapshot(tickers, 'Held Percent Institutions',axisamp=1.2)

info=stock_info("AAPL")

df=get_profile("AAPL")

tickers=['601398.SS','600036.SS','JPM','SMFG']
qr=compare_snapshot(tickers,'ROE',axisamp=1.7)


codetranslate("601658.SS")
codetranslate("600036.SS")

tickers=['601398.SS','601939.SS','601288.SS','601988.SS','601328.SS','600036.SS','601658.SS']
institution=compare_snapshot(tickers, 'Held Percent Institutions',axisamp=1.2)

dpidf=calc_dupont("601788.SS")
fsr2=get_financial_rates("601788.SS")
fsdf=get_financial_statements("601788.SS")
fsdft=fsdf.T

tickers=["601995.SS","601788.SS","300059.SZ","600030.SS","601878.SS"]
dpi=compare_dupont(tickers)

#======================================================================
tickers=["XPEV","000625.SZ","600104.SS","2238.HK","0175.HK","LI","NIO"]
gm=compare_snapshot(tickers,"Gross Margin",axisamp=1.9)
pm=compare_snapshot(tickers,"Profit Margin",axisamp=2)
#======================================================================
codetranslate("600030.SS")
codetranslate("601519.SS")
codetranslate("002502.SZ")
kdemo=candlestick_demo("600030.SS","2021-7-11","2021-7-15")
div=stock_dividend("600030.SS","2011-1-1","2021-7-15")
split=stock_split("600519.SS","2000-1-1","2021-7-15")

codename="SHANGHAI GREAT WISDOM CO LTD."

suffixlist=['Inc.','CO LTD','CO LTD.']
for sl in suffixlist:
    pos=codename.find(sl)
    if pos <= 0: continue
    else:
        codename=codename[:pos-1]
        print(codename)
        break






#======================================================================
#======================================================================
#======================================================================
#======================================================================
import os;os.chdir("S:/siat")
from siat import *

c_cn=economy_trend('2010-1-1','2020-1-1','China','Constant GDP',power=3)
c_cn=economy_trend('2010-1-1','2020-1-1','China','?',power=3)





codetranslate("0175.HK")
codetranslate("601825.SS")
codetranslate("601827.SS")
codetranslate("000003.SS")

codename=codetranslate("002003.SZ")
if codename[-2]==' ':
    codename=codename[:-3]

codetranslate("002003.SZ")
codetranslate("PLTR")

tickers=["XPEV","000625.SZ","600104.SS","2238.HK","0175.HK","LI","NIO"]
for t in tickers: print(codetranslate(t))

gm=compare_snapshot(tickers,"Gross Margin",axisamp=1.9)
#======================================================================
import akshare as ak

#列表中最后一个为最新名称
code="601825.SS"
suffix=code[-3:]
stock=code[:-3]
names = ak.stock_info_change_name(stock=stock)
if not (names is None):
    codename=names[-1]
else:
    codename=code



#======================================================================
import yfinance as yf

tp=yf.Ticker("XPEV")
dic=tp.info
current_name_eng=dic["shortName"]
