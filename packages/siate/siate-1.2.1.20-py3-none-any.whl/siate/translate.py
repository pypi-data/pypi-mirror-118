# -*- coding: utf-8 -*-
"""
本模块功能：SIAT公共转换函数
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2021年5月16日
最新修订日期：
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
def ectranslate(eword):
    """
    翻译英文专业词汇至中文，便于显示或绘图时输出中文而不是英文。
    输入：英文专业词汇。输出：中文专业词汇
    """
    import pandas as pd
    ecdict=pd.DataFrame([
        ['High','High'],['Low','Low'],['Open','Open'],['Close','Close'],
        ['Current Price','Current Price'],
        ['Volume','Volume'],['Adj Close','Adj Close'],['Daily Ret','Daily Return'],
        ['Daily Ret%','Daily Return%'],['Daily Adj Ret','调整日收益率'],
        ['Daily Adj Ret%','调整日收益率%'],['log(Daily Ret)','对数日收益率'],
        ['log(Daily Adj Ret)','对数调整日收益率'],['Weekly Ret','Weekly Return'],
        ['Weekly Ret%','Weekly Return%'],['Weekly Adj Ret','周调整收益率'],
        ['Weekly Adj Ret%','周调整收益率%'],['Monthly Ret','Monthly Return'],
        ['Monthly Ret%','Monthly Return%'],['Monthly Adj Ret','月调整收益率'],
        ['Monthly Adj Ret%','月调整收益率%'],['Quarterly Ret','Quarterly Return'],
        ['Quarterly Ret%','Quarterly Return%'],['Quarterly Adj Ret','季度调整收益率'],
        ['Quarterly Adj Ret%','季度调整收益率%'],['Annual Ret','Annual Return'],
        ['Annual Ret%','Annual Return%'],['Annual Adj Ret','年调整收益率'],
        ['Annual Adj Ret%','年调整收益率%'],['Exp Ret','Expanding Return'],
        ['Exp Ret%','Expanding Return%'],['Exp Adj Ret','持有调整收益率'],
        ['Exp Adj Ret%','持有调整收益率%'],
        
        ['Weekly Price Volatility','Weekly Price Volatility'],
        ['Weekly Adj Price Volatility','周调整股价波动风险'],
        ['Monthly Price Volatility','Monthly Price Volatility'],
        ['Monthly Adj Price Volatility','月调整股价波动风险'],
        ['Quarterly Price Volatility','Quarterly Price Volatility'],
        ['Quarterly Adj Price Volatility','季调整股价波动风险'],
        ['Annual Price Volatility','Annual Price Volatility'],
        ['Annual Adj Price Volatility','年调整股价波动风险'],  
        ['Exp Price Volatility','Expanding Price Volatility'], 
        ['Exp Adj Price Volatility','持有调整股价波动风险'],
        
        ['Weekly Ret Volatility','Weekly Return Volatility'],
        ['Weekly Ret Volatility%','Weekly Return Volatility%'],
        ['Weekly Adj Ret Volatility','周调整收益率波动风险'],
        ['Weekly Adj Ret Volatility%','周调整收益率波动风险%'],
        ['Monthly Ret Volatility','Monthly Return Volatility'],
        ['Monthly Ret Volatility%','Monthly Return Volatility%'],
        ['Monthly Adj Ret Volatility','月调整收益波动风险'],
        ['Monthly Adj Ret Volatility%','月调整收益波动风险%'],
        ['Quarterly Ret Volatility','Quarterly Return Volatility'],
        ['Quarterly Ret Volatility%','Quarterly Return Volatility%'],
        ['Quarterly Adj Ret Volatility','季调整收益率波动风险'],
        ['Quarterly Adj Ret Volatility%','季调整收益率波动风险%'],
        ['Annual Ret Volatility','Annual Return Volatility'],
        ['Annual Ret Volatility%','Annual Return Volatility%'],
        ['Annual Adj Ret Volatility','年调整收益率波动风险'], 
        ['Annual Adj Ret Volatility%','年调整收益率波动风险%'], 
        ['Exp Ret Volatility','Expanding Return Volatility'], 
        ['Exp Ret Volatility%','Expanding Return Volatility%'],
        ['Exp Adj Ret Volatility','持有调整收益率波动风险'],        
        ['Exp Adj Ret Volatility%','持有调整收益率波动风险%'],
        
        ['Weekly Ret LPSD','Weekly Return LPSD'],
        ['Weekly Ret LPSD%','Weekly Return LPSD%'],
        ['Weekly Adj Ret LPSD','周调整收益率波动损失风险'],
        ['Weekly Adj Ret LPSD%','周调整收益率波动损失风险%'],
        ['Monthly Ret LPSD','Monthly Return LPSD'],
        ['Monthly Ret LPSD%','Monthly Return LPSD%'],
        ['Monthly Adj Ret LPSD','月调整收益波动损失风险'],
        ['Monthly Adj Ret LPSD%','月调整收益波动损失风险%'],
        ['Quarterly Ret LPSD','Quarterly Return LPSD'],
        ['Quarterly Ret LPSD%','Quarterly Return LPSD%'],
        ['Quarterly Adj Ret LPSD','季调整收益率波动损失风险'],
        ['Quarterly Adj Ret LPSD%','季调整收益率波动损失风险%'],
        ['Annual Ret LPSD','Annual Return LPSD'],
        ['Annual Ret LPSD%','Annual Return LPSD%'],
        ['Annual Adj Ret LPSD','年调整收益率波动损失风险'], 
        ['Annual Adj Ret LPSD%','年调整收益率波动损失风险%'], 
        ['Exp Ret LPSD','Expanding Return LPSD'], 
        ['Exp Ret LPSD%','Expanding Return LPSD%'],
        ['Exp Adj Ret LPSD','持有调整收益率波动损失风险'],        
        ['Exp Adj Ret LPSD%','持有调整收益率波动损失风险%'],
        
        ['roll_spread','罗尔价差比率'],['amihud_illiquidity','阿米胡德非流动性'],
        ['ps_liquidity','P-S流动性'],    
        
        ['Gross Domestic Product','国内生产总值'],['GNI','国民总收入'],    
        
        ['zip','Zip'],['sector','Sector'],
        ['fullTimeEmployees','Fulltime Employees'],['Employees','Employees'],
        ['longBusinessSummary','业务介绍'],['city','City'],['phone','Phone'],
        ['state','State/Province'],['country','Country'],['companyOfficers','高管'],
        ['website','Website'],['address1','Address'],['industry','Industry'],
        ['previousClose','上个收盘价'],['regularMarketOpen','正常市场开盘价'],
        ['twoHundredDayAverage','200天均价'],['fax','传真'], 
        ['trailingAnnualDividendYield','年化股利率TTM'],
        ['payoutRatio','Payout Ratio'],['volume24Hr','24小时交易量'],
        ['regularMarketDayHigh','正常市场日最高价'],
        ['averageDailyVolume10Day','10天平均日交易量'],['totalAssets','总资产'],
        ['regularMarketPreviousClose','正常市场上个收盘价'],
        ['fiftyDayAverage','50天平均股价'],
        ['trailingAnnualDividendRate','Trailing Annual Dividend Rate'],['open','当日开盘价'],
        ['averageVolume10days','10日平均交易量'],['expireDate','失效日'],
        ['yield','收益率'],['dividendRate','Dividend Rate'],
        ['exDividendDate','股利除息日'],['beta','Beta'],
        ['startDate','开始日期'],['regularMarketDayLow','正常市场日最低价'],
        ['priceHint','价格提示'],['currency','Currency'],
        ['trailingPE','Trailing PE'],['regularMarketVolume','正常市场交易量'],
        ['marketCap','市值'],['averageVolume','平均交易量'],
        ['priceToSalesTrailing12Months','Price to Sales TTM'],
        ['TTM Price to Sales','Price to Sales TTM'],
        ['dayLow','当日最低价'],
        ['ask','卖出价'],['askSize','卖出价股数'],['volume','当日交易量'],
        ['fiftyTwoWeekHigh','52周最高价'],['forwardPE','Forward PE'],
        ['fiveYearAvgDividendYield','5年平均股利率'],
        ['fiftyTwoWeekLow','52周最低价'],['bid','买入价'],
        ['tradeable','今日是否可交易'],['dividendYield','Dividend Yield'],
        ['bidSize','买入价股数'],['dayHigh','当日最高价'],
        ['exchange','交易所'],['shortName','简称'],['longName','全称'],
        ['exchangeTimezoneName','交易所时区'],
        ['exchangeTimezoneShortName','交易所时区简称'],['quoteType','证券类别'],
        ['symbol','证券代码'],['messageBoardId','证券留言板编号'],
        ['market','证券市场'],['annualHoldingsTurnover','一年內转手率'],
        ['enterpriseToRevenue','市售率(EV/Revenue)'],['EV to Revenue','市售率(EV/Revenue)'],        
        ['Price to Book','Price to Book'],['beta3Year','3年贝塔系数'],
        ['profitMargins','Profit Margins'],['enterpriseToEbitda','企业价值/EBITDA'],
        ['EV to EBITDA','EV Multiples（EV/EBITDA)'],
        ['52WeekChange','52-week Price Change'],['morningStarRiskRating','晨星风险评级'],
        ['forwardEps','Forward EPS'],['revenueQuarterlyGrowth','季营收增长率'],
        ['sharesOutstanding','Shares Outstanding'],['fundInceptionDate','基金成立日'],
        ['annualReportExpenseRatio','年报费用比率'],['bookValue','每股净资产'],
        ['sharesShort','卖空股数'],['sharesPercentSharesOut','卖空股数/流通股数'],
        ['lastFiscalYearEnd','Last Fiscal Year End'],
        ['heldPercentInstitutions','Held Percent Institutions'],
        ['netIncomeToCommon','归属普通股股东净利润'],['trailingEps','Trailing EPS'],
        ['lastDividendValue','上次股利价值'],
        ['SandP52WeekChange','S&P Index 52-week Change'],['priceToBook','Price to Book'],
        ['heldPercentInsiders','Held Percent Insiders'],
        ['nextFiscalYearEnd','下个财年截止日期'],
        ['mostRecentQuarter','上个财季截止日期'],['shortRatio','空头净额比率'],
        ['sharesShortPreviousMonthDate','上月做空日期'],
        ['floatShares','可交易股数'],['enterpriseValue','企业价值'],
        ['threeYearAverageReturn','3年平均回报率'],['lastSplitDate','上个拆分日期'],
        ['lastSplitFactor','上次拆分比例'],
        ['earningsQuarterlyGrowth','Earnings Quarterly Growth'],['dateShortInterest','做空日期'],
        ['pegRatio','PEG Ratio'],['shortPercentOfFloat','空头占可交易股票比例'],
        ['sharesShortPriorMonth','上月做空股数'],
        ['fiveYearAverageReturn','5年平均回报率'],['regularMarketPrice','正常市场价'],
        ['logo_url','商标图标网址'],     ['underlyingSymbol','曾用代码'],     
        ['timeZoneShortName','时区简称'],['timeZoneFullName','时区全称'],
        ['exchangeName','Exchange'],['currentPrice','Current Price'],
        ['ratingYear','评估年度'],['ratingMonth','评估月份'],
        ['currencySymbol','币种符号'],['recommendationKey','Recommendation'],
        ['totalInsiderShares','内部人持股数'],['financialCurrency','Financial Currency'],
        ['currentRatio','Current Ratio'],['quickRatio','Quick Ratio'],
        ['debtToEquity','Debt to Equity%'],['ebitdaMargins','EBITDA Margins'],
        ['operatingMargins','Operating Margins'],['grossMargins','Gross Margins'],
        ['returnOnAssets','Return on Assets'],['returnOnEquity','Return on Equity'],
        ['ROA','ROA'],['ROE','ROE'],
        ['revenuePerShare','Revenue per Share'],['totalCashPerShare','Total Cash per Share'],
        ['revenueGrowth','Revenue Growth'],['earningsGrowth','Earnings Growth'],
        ['totalDebt','总负债'],['totalRevenue','总销售收入'],
        ['grossProfits','毛利润'],['ebitda','EBITDA'],
        ['operatingCashflow','经营现金流'],['freeCashflow','自由现金流'],
        ['totalCash','总现金流'],
        ['Total Asset Turnover','Total Asset Turnover'],['Fixed Asset Turnover','Fixed Asset Turnover'],
        ['PPE Residual','固定资产成新率'],
        ['Current Ratio','Current Ratio'],['Quick Ratio','Quick Ratio'],['Debt to Equity','Debt to Equity%'],
        ['Debt to Asset','Debt to Asset'],['Times Interest Earned','Times Interest Earned'],
        ['Inventory Turnover','Inventory Turnover'],['Receivable Turnover','Receivable Turnover'],
        ['BasicEPS','Basic EPS'],['Cashflow per Share','Cashflow per Share'],
        ['Profit Margin','Profit Margin'],['Gross Margin','Gross Margin'],
        ['EBITDA Margin','EBITDA Margin'],['Operating Margin','Operating Margin'],
        ['Trailing EPS','Trailing EPS'],['Trailing PE','Trailing PE'],['Forward PE','Forward PE'],
        ['Revenue Growth','Annual Revenue Growth Rate'],['Earnings Growth','Annual Earnings Growth Rate'],
        ['Earnings Quarterly Growth','季度盈余增长率'],
        ['IGR','Internal Growth Rate'],['SGR','Sustainable Growth Rate'],
        
        ['流动比','Current Ratio'],['速动比','Quick Ratio'],
        ['负债-权益比','Debt to Equity'],['负债-权益比%','Debt to Equity%'],
        ["实际所得税率%",'Actual Tax Rate%'],
        ["销售净利率",'Profit Margin'],["总资产周转率",'Total Asset Turnover'],
        ["权益乘数",'Equity Multiplier'],
        
        ['overallRisk','总风险指数'],
        ['boardRisk','董事会风险指数'],['compensationRisk','薪酬风险指数'],
        ['shareHolderRightsRisk','股东风险指数'],['auditRisk','审计风险指数'],
        
        ['totalEsg','Total ESG'],['Total ESG','Total ESG'],
        ['esgPerformance','ESG业绩评价'],
        ['peerEsgScorePerformance','ESG同业分数'],
        ['environmentScore','Environment Score'],['Environment Score','Environment Score'],
        ['peerEnvironmentPerformance','环保同业分数'],
        ['socialScore','Social Score'],['Social Score','Social Score'],
        ['peerSocialPerformance','社会责任同业分数'],
        ['governanceScore','Governance Score'],['Governance Score','Governance Score'],
        ['peerGovernancePerformance','公司治理同业分数'],['peerGroup','同业分组'],
        ['relatedControversy','相关焦点'],['Social Supply Chain Incidents','供应链事件'],
        ['Customer Incidents','客户相关事件'],['Business Ethics Incidents','商业道德事件'],
        ['Product & Service Incidents','产品与服务相关事件'],
        ['Society & Community Incidents','社会与社区相关事件'],
        ['Employee Incidents','雇员相关事件'],['Operations Incidents','运营相关事件'],
        ['peerCount','同业个数'],['percentile','同业所处分位数'],  
        
        ['ESGscore','ESG风险'],['ESGpercentile','ESG风险行业分位数%'],
        ['ESGperformance','ESG风险评价'],['EPscore','环保风险'],
        ['EPpercentile','环保风险分位数%'],['CSRscore','社会责任风险'],
        ['CSRpercentile','社会责任风险分位数%'],['CGscore','公司治理风险'],
        ['CGpercentile','公司治理风险分位数%'],
        ['Peer Group','业务分类'],['Count','数目'],     
        
        ['China','China'],['Japan','Japan'],['USA','USA'],['India','India'],
        ['Russia','Russia'],['Korea','Korea'],
        
        ['Gross Domestic Product','国内生产总值'],['GDP','国内生产总值'],  
        ['CNP GDP','GDP（美元不变价格）'],['Constant GDP','GDP（本币不变价格）'],
        ['Current Price Gross Domestic Product','国内生产总值'],
        ['Constant GDP Per Capita','人均GDP（本币不变价格）'],
        ['CNP GDP Per Capita','人均GDP（美元不变价格）'],
        ['Constant Price GDP Per Capita','人均GDP'],
        ['GNP','国民生产总值'],['GNP Ratio','GNP(GNI)与GDP的比例'],
        ['GNI/GDP Ratio','GNP(GNI)与GDP的比例'],
        ['Ratio of GNP to GDP','GNP(GNI)与GDP之间的比例关系'],
        
        ['CPI','消费者价格指数'],['YoY CPI','CPI%（同比）'],
        ['MoM CPI','CPI%（环比）'],['Constant CPI','Constant CPI%'],
        ['Consumer Price Index','消费者价格指数'],
        ['Consumer Price Index: All Items','All Item CPI'],
        ['Consumer Price Index: All Items Growth Rate','全要素CPI增速'],
        ['PPI','生产者价格指数'],['YoY PPI','PPI%（同比）'],
        ['MoM PPI','PPI%（环比）'],['Constant PPI','PPI%（本币不变价格）'],
        ['Producer Prices Index: Industrial Activities','工业活动PPI'],
        ['Producer Prices Index: Total Industrial Activities','全部工业活动PPI'],
        
        ['Exchange Rate','汇率'],
        ['M0','流通中现金M0供应量'],['M1','狭义货币M1供应量'],['M2','广义货币M2供应量'],
        ['M3','金融货币M3供应量'],
        ['National Monetary Supply M0','流通中现金M0供应量'],
        ['National Monetary Supply M1','狭义货币M1供应量'],
        ['National Monetary Supply M2','广义货币M2供应量'],
        ['National Monetary Supply M3','金融货币M3供应量'],
        
        ['Discount Rate','贴现率%'],
        ['Central Bank Discount Rate','中央银行贴现率'],
        
        ['Immediate Rate','即期利率%'],
        ['Immediate Rates: Less than 24 Hours: Interbank Rate','银行间即期利率（24小时内）'],  
        
        ['Local Currency/USD Foreign Exchange Rate','本币/美元汇率'],  
        ['USD/Local Currency Foreign Exchange Rate','美元/本币汇率'],['Euro','欧元'],
        
        ['Daily','daily'],['Monthly','monthly'],['Quarterly','quarterly'],['Annual','annual'],
        
        ['Stock Market Capitalization to GDP','基于股市总市值的经济金融深度'],
        ['SMC to GDP','股市总市值/GDP'],
        
        ['Currency Value','Currency value'],['Currency Purchasing Power Based on CPI','Currency Purchasing Power Based on CPI'],
        
        ['Portfolio','投资组合'],['Portfolio_EW','等权重组合'],['Portfolio_OMCap','流通市值权重组合'],
        ['Portfolio_MSR','MSR组合'],['Portfolio_GMV','GMV组合'],
        
        ], columns=['eword','cword'])

    try:
        cword=ecdict[ecdict['eword']==eword]['cword'].values[0]
    except:
        #未查到翻译词汇，返回原词
        cword=eword
   
    return cword

if __name__=='__main__':
    eword='Exp Adj Ret'
    print(ectranslate('Annual Adj Ret%'))
    print(ectranslate('Annual*Adj Ret%'))


#==============================================================================
def codetranslate(code):
    """
    翻译证券代码为证券名称。
    输入：证券代码。输出：证券名称
    """
    import pandas as pd
    codedict=pd.DataFrame([
            
        #股票：地产
        ['000002.SZ','Wanke A'],['600266.SS','城建发展'],['600376.SS','首开股份'],
        ['600340.SS','华夏幸福'],['600606.SS','绿地控股'],
        
        #股票：白酒
        ['600519.SS','Moutai'],['000858.SZ','Wuliangye'],['000596.SZ','Gujinggong'],
        ['000568.SZ','Luzhou Laojiao'],['600779.SS','Suijingfang'],['002304.SZ','Yanghe'],
        ['000799.SZ','Jiuguijiu'],['603589.SS','Kouzijiao'],['600809.SS','Shanxi Fenjiu'],
        
        #股票：银行
        ['601398.SS','ICBC A'],['601939.SS','CCB A'],
        ['601288.SS','ABC A'],['601988.SS','BOC A'],
        ['600000.SS','SPDB'],['601328.SS','BCOMM A'],
        ['600036.SS','CMB'],['000776.SZ','GDB'],
        ['601166.SS','Industrial Bank'],['601169.SS','Bank of Beijing'],
        ['600015.SS','HUaxia Bank'],['601916.SS','Zheshang Bank'],
        ['600016.SS','Minsheng Bank'],['000001.SZ','Pingan Bank'],
        ['601818.SS','Everbright Bank'],['601998.SS','CITIC Bank'],
        ['601229.SS','Bank of Shanghai'],['601658.SS','PSBC'],
        
        ['1398.HK','ICBC HK'],['0939.HK','CCB HK'],
        ['1288.HK','ABC HK'],['0857.HK','Petro China HK'],
        ['3988.HK','BOC HK'],['BANK OF CHINA','Bank of China'],
        
        ['CICHY','CCB US'],['CICHF','CCB US'],
        ['ACGBY','ABC US'],['ACGBF','ABC US'],
        ['IDCBY','ICBC US'],['IDCBF','ICBC US'],
        ['BCMXY','BCOMM US'],
        
        ['BAC','Bank of America'],['Bank of America Corporation','Bank of America'],
        ['JPM','JP Morgan Chase'],['JP Morgan Chase & Co','JP Morgan Chase'],
        ['WFC','Wells Fargo'],
        ['MS','Morgan Stanley'],['Morgan Stanley','Morgan Stanley'],
        ['USB','U.S. Bancorp'],['U','U.S. Bancorp'],
        ['TD','Toronto-Dominion Bank'],['Toronto Dominion Bank','Toronto-Dominion Bank'],
        ['PNC','PNC Financial'],['PNC Financial Services Group','PNC Financial'],
        ['BK','Bank of New York Mellon'],['The Bank of New York Mellon Cor','Bank of New York Mellon'],    
        ['GS','Goldman Sachs'],['C','Citigroup'],
        
        ['8306.T','三菱日联金融'],['MITSUBISHI UFJ FINANCIAL GROUP','三菱日联金融'],
        ['8411.T','日股瑞穗金融'],['MIZUHO FINANCIAL GROUP','瑞穗金融'],
        ['7182.T','日本邮政银行'],['JAPAN POST BANK CO LTD','日本邮政银行'], 

        ['0005.HK','HSBC'],['HSBC HOLDINGS','HSBC'],
        ['2888.HK','Standard Chartered'],['STANCHART','Standard Chartered'],  
        
        ['UBSG.SW','UBS'],        

        #股票：高科技
        ['AAPL','Apple'],['Apple','Apple'],['DELL','Dell'],['IBM','IBM'],
        ['MSFT','Microsoft'],['Microsoft','Microsoft'],['HPQ','HP'],['AMD','AMD'],
        ['NVDA','NVidia'],['INTC','Intel'],['QCOM','Qualcomm'],['BB','BlackBerry'],
        
        #股票：电商、互联网        
        ['AMZN','Amazon'],['Amazon','Amazon'],
        ['EBAY','eBay'],['eBay','eBay'],['FB','Facebook'],['ZM','ZOOM'],
        ['GOOG','Alphabet'],['TWTR','Twitter'],
        ['VIPS','Vipshop'],['Vipshop','Vipshop'],
        ['PDD','PDD'],['Pinduoduo','PDD'],        
        ['BABA','Alibaba US'],['Alibaba','Alibaba US'],
        ['JD','JD US'],
        ['BIDU','Baidu'],['NTES','NetEase US'],['9999.HK','NetEase HK'],
        
        ['0700.HK','Tecent Holdings'],['TENCENT','Tecent Holdings'],
        ['9988.HK','Alibaba HK'],['BABA-SW','Alibaba HK'],
        ['9618.HK','JD HK'],['JD-SW','JD HK'], 
        
        #股票：石油、矿业
        ['SLB','Schlumberger'],['BKR','Baker Hughes'],['HAL','Halliburton'],
        ['WFTUF','Weatherford'],
        ['OXY','Occidental Petroleum'],['COP','Conoco Phillips'],
        ['FCX','Freeport-McMoRan'], ['AEM','Agnico Eagle Mines'],   
        ['XOM','Exxon Mobil'],['2222.SR','Aramco'],
        ['BP','BP'],['RDSA.AS','Royal Dutch Shell'],
        ['1605.T','Inpex'],['5020.T','ENEOS'],['5713.T','Sumitomo Metal Mining'],
        ['COP','Conoco Phillips'],['NEM','Newmont Goldcorp'],['SCCO','Southern Copper'],
        ['RGLD','Royal Gold'],['AA','Alcoa'],['CLF','Cleveland-Cliffs'],
        ['BTU','Peabody Energy'],['KMI','Kinder Morgan'],['TRP','TC Energy'],
        ['SU','Suncor Energy'],['ENB','Enbridge'],['CNQ','Canadian Natural Resources'],
        ['WMB','The Williams Companies'],
        
        
        ['601857.SS','Petro China A'],['PTR','Petro China US'],
        ['0857.HK','Petro China HK'],['PETROCHINA','Petro China'],
        
        ['0883.HK','CNOOC HK'],['601808.SS','China Oilfield Services A'],
        ['2883.HK','China Oilfield Services HK'],['600583.SS','Offshore Oil Engineering A'],
        ['600968.SS','CNOOC Energy Tech & Serv A'],
        
        ['600028.SS','Sinopec A'],['0386.HK','Sinopec HK'],
        ['600871.SS','Sinopec Oilfield Serv A'],['1033.HK','Sinopec Oilfield Serv HK'],
        
        ['600339.SS','China Petroleum Engineering A'],
        
        ['3337.HK','安东油服港股'],['603619.SS','中曼石油A股'],['002476.SZ','宝莫股份A股'],
        ['002828.SZ','贝肯能源A股'],['300164.SZ','通源石油A股'],['300084.SZ','海默科技A股'],
        ['300023.SZ','宝德股份A股'],
        
        #股票：汽车
        ['F','Ford Motor'],['GM','General Motors'],['TSLA','Tesla'],
        ['7203.T','Toyota Motor JP'],['7267.T','Honda Motor JP'],['7201.T','Nissan Motor JP'], 
        ['DAI.DE','Daimler AG'],['BMW.DE','BMW AG'],
        ['XPEV','XPeng Auto'],['LI','Li Auto'],['0175.HK','Geely Auto'],['NIO','NIO Auto'],
        ['2238.HK','Guangzhou Auto'],['000625.SZ','Changan Auto'],['600104.SS','SAIC Motor'],
        
        #股票：制药
        ['LLY','Eli Lilly'],['Eli','Eli Lilly'],
        ['JNJ','Johnson & Johnson'],['Johnson','Johnson & Johnson'],
        ['VRTX','Vertex'],['Vertex','Vertex'],
        ['PFE','Pfizer'],['Pfizer','Pfizer'],
        ['MRK','Merck'],['Merck','Merck'],
        ['NVS','Novartis'],['Novartis','Novartis'],
        ['AMGN','Amgen'],['Amgen','Amgen'],
        ['SNY','Sanofi'],['Sanofi','Sanofi'],
        ['AZN','AstraZeneca'],['MRNA','Moderna'],
        ['NBIX','Neurorine'],['Neurocrine','Neurorine'],
        ['REGN','Regeneron'],['Regeneron','Regeneron'],
        ['PRGO','Perrigo'],['Perrigo','Perrigo'],
        
        #股票：教育、视频
        ['BILI','Bilibili'],['TAL','TAL Education'],['EDU','New Oriental Education'],        
        ['IQ','iQIYI'],['HUYA','HUYA'],['1024.HK','Kuaishou'],
        
        #股票：服饰，鞋帽，化妆品，体育，奢侈品
        ['002612.SZ','朗姿股份'],['002832.SZ','BIEM.L.FDLKK Garment'],
        ['002291.SZ','Saturday Garment'],['600398.SS','Hla Garment'],
        ['600400.SS','红豆股份'],['300005.SZ','Toread Garment'],
        ['603877.SS','太平鸟'],['002563.SZ','森马服饰'],
        ['002154.SZ','报喜鸟'],['002029.SZ','七匹狼'],
        ['601566.SS','九牧王'],['600107.SS','美尔雅'],
        ['603116.SS','红蜻蜓'],['002503.SZ','搜于特'],
        ['002193.SZ','如意集团'],['603001.SS','奥康国际'],
        ['300979.SZ','C华利'],['002269.SZ','美邦服饰'],
        ['600884.SS','杉杉股份'],['600177.SS','雅戈尔'],
        ['300526.SZ','中潜股份'],['601718.SS','际华集团'],
        ['603157.SS','拉夏贝尔A股'],['600295.SS','鄂尔多斯'],
        ['002293.SZ','罗莱生活'],['603587.SS','地素时尚'],
        ['002404.SZ','嘉欣丝绸'],['600612.SS','老凤祥'],
        ['300577.SZ','开润股份'],['600137.SS','浪莎股份'],
        
        ['2331.HK','Li Ning'],['2020.HK','ANTA Sports'],['1368.HK','特步国际'],
        ['1361.HK','361度'],['6116.HK','拉夏贝尔港股'],['3306.HK','江南布衣'],
        ['2298.HK','都市丽人'],['1388.HK','安莉芳'],['1749.HK','杉杉品牌'],
        ['1234.HK','中国利郎'],['2030.HK','卡宾'],['0709.HK','佐丹奴国际'],
        ['3998.HK','Bosideng'],['0592.HK','堡狮龙'],['2313.HK','Shenzhou International'],
        ['6110.HK','滔博'],['3813.HK','宝胜国际'],['6288.HK','UNI QLO HK'],
        ['1913.HK','普拉达'],['0551.HK','裕元集团'],['2399.HK','虎都'],
        ['2232.HK','晶苑国际'],['1146.HK','中国服饰控股'],
        
        ['4911.T','Shiseido'],['4452.T','KAO'],
        ['9983.T','UNI QLO JP'],['7453.T','日股无印良品'],   
        
        ['CDI.PA','Christian Dior'],['DIO.F','Christian Dior'],['HMI.F','Hermes'],
        
        #股票：其他
        ['PG','P & G'],['KO','Coca-Cola'],['PEP','Pepsi-Cola'],
        ['BRK.A','伯克希尔'],['BRK.B','伯克希尔'],['Berkshire','伯克希尔'],
        ['COST','Costco'],['WMT','Walmart'],['DIS','Walt Disney'],['BA','Boeing'],

        ['000651.SZ','格力电器A股'],['000333.SZ','美的集团A股'],

        ['0992.HK','Lenovo Group HK'],['LENOVO GROUP','Lenovo Group'],
        ['1810.HK','Xiaomi HK'],
        ['1166.HK','Solartech HK'],['0273.HK','Mason Group HK'],

        ['2330.TW','TSMC'],['2317.TW','Hon Hai Precision'],['2474.TW','Catcher Technology'],
        ['3008.TW','LARGAN Precision'],['2454.TW','MediaTek'],  
        
        ['6758.T','Sony JP'],
        
        ['005930.KS','Samsung KS'],
        
        ['TCS.NS','Tata Consulting'],
        
        #股票：指数==============================================================
        ['000300.SS','CSI300 Index'],['399300.SS','CSI300 Index'],
        ['000001.SS','SSE Composite Index'],
        ['399001.SZ','Shenzhen Component Index'],['399102.SZ','GEM Composite Index'],
        ['399101.SZ','SMB Composite Index'],
        ['000016.SS','SSE50 Index'],['000132.SS','SSE100 Index'],
        ['000133.SS','SSE150 Index'],['000010.SS','SSE180 Index'],
        ['000688.SS','STAR50 Index'],['000043.SS','SSE Mega-cap Index'],
        ['000044.SS','SSE Mid-cap Index'],['000046.SS','SSE Mid-small Cap Index'],
        ['000045.SS','SSE Small-cap Index'],['000004.SS','上证工业指数'],
        ['000005.SS','上证商业指数'],['000006.SS','上证地产指数'],
        ['000007.SS','上证公用指数'],['000038.SS','上证金融指数'],
        ['000057.SS','上证全指成长指数'],['000058.SS','上证全指价值指数'],
        ['000019.SS','上证治理指数'],['000048.SS','上证责任指数'],
        
        ['000002.SS','SSE A Share Index'],['000003.SS','SSE B Share Index'],
        ['399107.SZ','SZSE A Share Index'],['399108.SZ','SZSE B Share Index'],
        ['399106.SZ','SZSE Composite Index'],['399004.SZ','SZSE100 Index'],
        ['399012.SZ','GEM300 Index'],
        
        ['399232.SZ','深证采矿业指数'],['399233.SZ','深证制造业指数'],
        ['399234.SZ','深证水电煤气指数'],['399236.SZ','深证批发零售指数'],
        ['399237.SZ','深证运输仓储指数'],['399240.SZ','深证金融业指数'],
        ['399241.SZ','深证房地产指数'],['399244.SZ','深证公共环保指数'],
        
        ['000903.SS','CSI100 Index'],['399903.SZ','中证100指数'],
        ['000904.SS','CSI200 Index'],['399904.SZ','中证200指数'],
        ['000905.SS','CSI500 Index'],['399905.SZ','中证500指数'],
        ['000907.SS','CSI700 Index'],['399907.SZ','中证700指数'],
        ['000906.SS','CSI800 Index'],['399906.SZ','中证800指数'],
        ['000852.SS','CSI1000 Index'],['399852.SZ','中证1000指数'],
        ['000985.SS','中证全指指数'],['399985.SZ','中证全指指数'],
        
        ['000012.SS','SSE Treasury Bond Index'],['000013.SS','SSE Enterprise Bond Index'],
        ['000022.SS','SSE Corporate Bond Index'],['000061.SS','上证企债30指数'],
        ['000116.SS','SSE Credit Bond 100 Index'],['000101.SS','上证5年期信用债指数'],

        ['^GSPC','S&P500 Index'],['^DJI','Dow Jones 30 Index'],
        ['WISGP.SI','富时新加坡指数'], ['^STI','新加坡海峡时报指数'],
        ['^IXIC','NASDAQ Composite Index'],['^FTSE','FTSE100 Index'],
        ['FVTT.FGI','富时越南指数'],['^RUT','Russell2000 Index'],
        ['^HSI','Hang Seng Index'],['^HSIL','Hang Seng Volatility Index'],
        ['^N225','Nikkei225 Index'],
        ['WIKOR.FGI','富时韩国指数'],['^KS11','KOSPI Composite Index'],
        ['^KOSPI','KOSPI Composite Index'],['^BSESN','BSE SENSEX'],
        ['^FCHI','CAC40 Index'],['^GDAXI','DAX Performance Index'], 
        ['IMOEX.ME','MOEX Russian Index'], ['^VIX','CBOE Volatility Index'],
        
        ['^HSCE','恒生H股指数'],['^HSNC','恒生工商业指数'],['^HSNU','恒生公用行业指数'], 
        ['^TWII','TSEC Weighted Index'], 
        
        #债券==================================================================
        ['sh019521','15国债21'],['sh019640','20国债10'],['sh019654','21国债06'],
        ['sz128086','国轩转债'],['sz123054','思特转债'],['sz123029','英科转债'],
        ['sz123027','蓝晓转债'],
        ['^IRX','13 Week T-Bill Yield%'],['^FVX','Treasury Yield 5 Years%'],
        ['^TNX','Treasury Yield 10 Years%'],['^TYX','Treasury Yield 30 Years%'],
        
        #基金==================================================================
        ['000595','嘉实泰和混合基金'],['000592','建信改革红利股票基金'],
        ['050111','博时信债C'],['320019','诺安货币B基金'],
        ['510580','易方达中证500ETF'],['510210.SS','上证综指ETF'],
        ["510050.SS",'上证50ETF基金'],['510880.SS','上证红利ETF基金'],
        ["510180.SS",'上证180ETF基金'],['159901.SZ','深证100ETF基金'],
        ["159902.SZ",'深证中小板ETF基金'],['159901.SZ','深证100ETF基金'],
        ["SPY",'SPDR SP500 ETF'],['SPYD','SPDR SP500 Div ETF'],
        ["SPYG",'SPDR SP500 Growth ETF'],['SPYV','SPDR SP500 Value ETF'],
        ["VOO",'Vanguard SP500 ETF'],['VOOG','Vanguard SP500 Growth ETF'],
        ["VOOV",'Vanguard SP500 Value ETF'],['IVV','iShares SP500 ETF'],        
        ["DGT",'SPDR Global Dow ETF'],['ICF','iShares C&S REIT ETF'], 
        ["FRI",'FT S&P REIT Index Fund'],['IEMG','iShares核心MSCI新兴市场ETF'],    
        ['245710.KS','KINDEX越南VN30指数ETF'],['2801.HK','iShares核心MSCI中国指数ETF'],

        #期货==================================================================
        ["HG=F",'COMEX铜矿石期货'],["CL=F",'NYM原油期货'],
        ["S=F",'CBT大豆期货'],["C=F",'CBT玉米期货'],
        ["ES=F",'CME标普500指数期货'],["YM=F",'CBT道指期货'],
        ["NQ=F",'CME纳指100期货'],["RTY=F",'罗素2000指数期货'],
        ["ZB=F",'10年期以上美债期货'],["ZT=F",'2年期美债期货'],
        ["ZF=F",'5年期美债期货'],["ZN=F",'10年期美债期货'],   
        
        #======================================================================
        #=新加入
        #======================================================================
        # 白酒行业
        ['603589.SS','口子窖'],['000568.SZ','泸州老窖'],['000858.SZ','五粮液'],
        ['600519.SS','贵州茅台'],['000596.SZ','古井贡酒'],['000799.SZ','酒鬼酒'],
        ['600809.SS','山西汾酒'],['600779.SS','水井坊'],

        # 房地产行业
        ['000002.SZ','万科A'],['600048.SS','保利地产'],['600340.SS','华夏幸福'],
        ['000031.SZ','大悦城'],['600383.SS','金地集团'],['600266.SS','城建发展'],
        ['600246.SS','万通发展'],['600606.SS','绿地控股'],['600743.SS','华远地产'],
        ['000402.SZ','金融街'],['000608.SZ','阳光股份'],['600376.SS','首开股份'],
        ['000036.SZ','华联控股'],['000620.SZ','新华联'],['600663.SS','陆家嘴'],

        # 银行业
        ['601328.SS','交通银行'],['601988.SS','中国银行'],['600015.SS','华夏银行'],
        ['601398.SS','工商银行'],['601169.SS','北京银行'],['601916.SS','浙商银行'],
        ['601288.SS','农业银行'],['601229.SS','上海银行'],['600016.SS','民生银行'],
        ['601818.SS','光大银行'],['601658.SS','邮储银行'],['600000.SS','浦发银行'],
        ['601939.SS','建设银行'],['601998.SS','中信银行'],['601166.SS','兴业银行'],
        ['600036.SS','招商银行'],['002142.SZ','宁波银行'],['000001.SZ','平安银行'],

        # 纺织服装行业
        ['002612.SZ','朗姿股份'],['601566.SS','九牧王'],['002269.SZ','美邦服饰'],
        ['600398.SS','海澜之家'],['600137.SS','浪莎股份'],['603001.SS','奥康国际'],
        ['603116.SS','红蜻蜓'],['002291.SZ','星期六'],['002832.SZ','比音勒芬'],
        ['600400.SS','红豆股份'],['300005.SZ','探路者'],['603877.SS','太平鸟'],
        ['002563.SZ','森马服饰'],['002154.SZ','报喜鸟'],['600177.SS','雅戈尔'],
        ['002029.SZ','七匹狼'],

        # 物流行业
        ['002352.SZ','顺丰控股'],['002468.SZ','申通快递'],['600233.SS','圆通速递'],
        ['002120.SZ','韵达股份'],['603128.SS','华贸物流'],['603056.SS','德邦股份'],
        ['601598.SS','中国外运'],['603967.SS','中创物流'],['603128.SS','华贸物流'],

        # 券商行业
        ['601995.SS','中金公司'],['601788.SS','光大证券'],['300059.SZ','东方财富'],
        ['600030.SS','中信证券'],['601878.SS','浙商证券'],['600061.SS','国投资本'],
        ['600369.SS','西南证券'],['600837.SS','海通证券'],['601211.SS','国泰君安'],
        ['601066.SS','中信建投'],['601688.SS','华泰证券'],['000776.SZ','广发证券'],
        ['000166.SZ','申万宏源'],['600999.SS','招商证券'],['002500.SZ','山西证券'],
        ['601555.SS','东吴证券'],['000617.SZ','中油资本'],['600095.SS','湘财股份'],
        ['601519.SS','大智慧'],

        # 中国啤酒概念股
        ['600600.SS','青岛啤酒'],['600132.SS','重庆啤酒'],['002461.SZ','珠江啤酒'],
        ['000729.SZ','燕京啤酒'],['600573.SS','惠泉啤酒'],['000929.SZ','兰州黄河'],
        ['603076.SS','乐惠国际'],

        # 建筑工程概念股
        ['601186.SS','中国铁建'],['601668.SS','中国建筑'],['601800.SS','中国交建'],
        ['601789.SS','宁波建工'],['601669.SS','中国电建'],['000498.SZ','山东路桥'],
        ['600170.SS','上海建工'],['600248.SS','陕西建工'],['600502.SS','安徽建工'],
        ['600284.SS','浦东建设'],['603815.SS','交建股份'],['600039.SS','四川路桥'],

        # 民用航空概念股
        ['600221.SS','海南航空'],['603885.SS','吉祥航空'],['600115.SS','中国东航'],
        ['600029.SS','南方航空'],['601021.SS','春秋航空'],['601111.SS','中国国航'],
        ['002928.SZ','华夏航空'],

        # 家电概念股
        ['600690.SS','海尔智家'],['600060.SS','海信视像'],['000333.SZ','美的集团'],
        ['000404.SZ','长虹华意'],['000651.SZ','格力电器'],['000521.SZ','长虹美菱'],
        ['603868.SS','飞科电器'],['600839.SS','四川长虹'],['000921.SZ','海信家电'],
        ['002035.SZ','华帝股份'],['002242.SZ','九阳股份'],['600336.SS','澳柯玛'],
        ['600854.SS','春兰股份'],['000418.SZ','小天鹅A'],['002508.SZ','老板电器'],
        ['000810.SZ','创维数字'],['603551.SS','奥普家居'],['002959.SZ','小熊电器'],
        ['000100.SZ','TCL科技'],['002032.SZ','苏泊尔'],['000016.SZ','深康佳A'],
        ['600690.SS','青岛海尔'],['000541.SZ','佛山照明'],['603515.SS','欧普照明'],

        # 体育用品概念股
        ['2020.HK','安踏体育'],['2331.HK','李宁'],['1368.HK','特步国际'],
        ['1361.HK','361度'],['ADS.DE','ADIDAS'],['NKE','NIKE'],
        ['8022.T','MIZUNO'],['PUM.DE','PUMA SE'],['FILA.MI','FILA'],
        ['SKG.L','Kappa'],['7936.T','ASICS'],

        # 新加坡著名股票
        ['D05.SI','星展银行DBS'],['Z74.SI','新加坡电信'],['O39.SI','华侨银行'],
        ['U11.SI','大华银行'],['C6L.SI','新加坡航空'],['CC3.SI','Starhub'],
        ['S08.SI','新加坡邮政'],['F34.SI','WILMAR'],['C31.SI','CapitaLand'],        


        ], columns=['code','codename'])
    
    codename=code
    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译词汇，查找akshare和雅虎财经上的短名称，稍慢
        try:
            codename=securities_name(code)
        except:
            pass
   
    return codename

if __name__=='__main__':
    code='GOOG'
    print(codetranslate('000002.SZ'))
    print(codetranslate('9988.HK'))

#==============================================================================
def securities_name(code):
    """
    功能：搜索证券代码的名称，先中文后英文
    """
    codename=code
    
    #搜索国内股票的曾用名
    import akshare as ak
    suffix=code[-3:]
    stock=code[:-3]
    if suffix in ['.SS','.SZ']:
        try:
            names = ak.stock_info_change_name(stock=stock)
            if not (names is None):
                #列表中最后一个为最新名称
                codename=names[-1]
                return codename
        except:
            pass
        
    #不是国内股票或中文名称未查到
    if not (suffix in ['.SS','.SZ']) or (codename==code):
        try:
            import yfinance as yf
            tp=yf.Ticker(code)
            dic=tp.info
            codename=dic["shortName"]  
                
            #若倒数第2位是空格，最后一位只有一个字母，则截取
            if codename[-2]==' ':
                codename=codename[:-2]
                
            #若最后几位在下表中，则截取
            sl1=['Inc.','CO LTD','CO LTD.','CO. LTD.']
            sl2=['Co.,Ltd','Co.,Ltd.','Co., Ltd','Limited']
            sl3=['CO','Corporation']
            suffixlist=sl1+sl2+sl3
            for sl in suffixlist:
                pos=codename.find(sl)
                if pos <= 0: continue
                else:
                    codename=codename[:pos-1]
                    #print(codename)
                    break 
        except:
            pass
        
        return codename

if __name__=='__main__':
    securities_name('000002.SZ')
    securities_name('002504.SZ')
    securities_name('002503.SZ')
    securities_name('XPEV')
    securities_name('IBM')
    securities_name('NIO')
    securities_name('600519.SS')
    securities_name('601519.SS')
    securities_name('MSFT')
    
#==============================================================================
def texttranslate(code):
    """
    翻译文字为中文或英文。
    输入：文字。输出：翻译成中文或英文
    """
    import pandas as pd
    codedict=pd.DataFrame([
            
        ['数据来源: 雅虎财经,','Source: Yahoo Finance,'],['数据来源：雅虎财经，','Source: Yahoo Finance,'],
        ["证券快照：","证券快照："],
        ["证券价格走势图：","Price Movement Trend: "],
        ["证券收益率波动损失风险走势图：","证券收益率波动损失风险走势图："],
        ["证券指标走势对比图：","Securities Trend: "],
        ["证券价格走势蜡烛图演示：","Securities K-line Diagram："],
        ["股票分红历史","股票分红历史"],
        ["股票:","Stock:"],["历史期间:","Period:"],
        ['序号','No.'],['日期','Date'],['星期','Weekday'],['股息','Dividend'],
        ["股票分拆历史","股票分拆历史"],
        ['分拆比例','Split'],
        ["公司基本信息","Corporate Profile"],
        ["公司高管信息","Corporate Management"],
        ["公司高管:","Senior Management:"],
        ["基本财务比率TTM","Financial Ratios"],
        ["财报主要项目","财报主要项目"],
        ["基本市场比率","Market Ratios"],
        ["一般风险指数","一般风险指数"],
        ["(指数越小风险越低)","(指数越小风险越低)"],
        ["可持续发展风险","可持续发展风险"],
        ["(分数越小风险越低)","(分数越小风险越低)"],
        ['\b岁 (生于','years old (born '],
        ['总薪酬','Total Compensation'],["均值","均值"],
        ["投资组合的可持续发展风险","投资组合的可持续发展风险"],
        ["投资组合:","投资组合:"],
        ["ESG评估分数:","ESG评估分数:"],
        ["   EP分数(基于","   EP分数(基于"],
        ["   CSR分数(基于","   CSR分数(基于"],
        ["   CG分数(基于","   CG分数(基于"],
        ["   ESG总评分数","   ESG总评分数"],
        ["注：分数越高, 风险越高.","注：分数越高, 风险越高."],
        
        ['趋势线','Trend'],["(趋势线)",'(Trend)'],["价格",'Price'],
        
        ["中国债券市场月发行量","中国债券市场月发行量"],
        ["数据来源：中国银行间市场交易商协会(NAFMII)，","数据来源：中国银行间市场交易商协会(NAFMII)，"],
        ["发行量","发行量"],["金额(亿元)","金额(亿元)"],
        ["中国银行间市场债券现券即时报价","中国银行间市场债券现券即时报价"],
        ["，前","，前"],["名）***","名）***"],
        ["中国债券市场月发行量","中国债券市场月发行量"],
        ["价格","Price"],["成交量","Volume"],
        
        ["按照收益率从高到低排序","Yield: High to Low"],
        ["按照发行时间从早到晚排序","Issue Date: Early First"],
        ["按照发行时间从晚到早排序","Issue Date: Late First"],
        ["按照报价机构排序","by Price Offering Institutions"],
        ["按照涨跌幅从高到低排序","Change: High to Low"],
        ["按照涨跌幅从低到高排序","Change: Low to High"],
        ["按照交易时间排序","by Transaction Time"],
        ["按照成交量从高到低排序","Volume: High to Low"],
        ["按照成交量从低到高排序","Volume: Low to High"],
        ["按照成交价从高到低排序","Deal Price: High to Low"],
        ["按照成交价从低到高排序","Deal Price: Low to High"],
        
        ['时间','Time'],['债券代码','Code'],        
        ['债券名称','Name'],['成交价','Deal Price'],['涨跌(元)','Change'],
        ['开盘价','Open'],['最高价','High'],['最低价','Low'],
        ['买入价','Bid'],['卖出价','Ask'],['收盘价','Close'],
        ["沪深交易所债券市场现券即时成交价（","Exchange Bond Market Deal Price ("],
        
        ["数据来源：新浪财经，","Data source: Sina Finance, "],
        ['沪深债券收盘价历史行情：','Exchange Bond Price Trend: '],
        ["按照代码从小到大排序","按照代码从小到大排序"],
        ["按照代码从大到小排序","按照代码从大到小排序"],
        ["沪深交易所可转债现券即时行情（","沪深交易所可转债现券即时行情（"],
        ['沪深市场可转债收盘价历史行情：','沪深市场可转债收盘价历史行情：'],
        ["政府债券列表","政府债券列表"],
        ['中国','中国'],['美国','美国'],['日本','日本'],['韩国','韩国'],
        ['泰国','泰国'],['越南','越南'],['印度','印度'],['德国','德国'],
        ['法国','法国'],['英国','英国'],['意大利','意大利'],['西班牙','西班牙'],
        ['俄罗斯','俄罗斯'],['加拿大','加拿大'],['澳大利亚','澳大利亚'],
        ['新西兰','新西兰'],['新加坡','新加坡'],['马来西亚','马来西亚'],
        
        ['全球政府债券收盘价历史行情：','全球政府债券收盘价历史行情：'],
        ["数据来源：英为财情，","数据来源：英为财情，"],
        ['到期收益率变化','Change of YTM'],
        ['到期收益率%','YTM%'],
        ["债券价格与到期收益率的关系","Bond Price vs. YTM"],
        ["债券价格","Price"],
        ["到期收益率及其变化幅度","YTM and changes "],
        ["债券面值","Face value="],
        ["，票面利率",", Coupon rate="],
        ["每年付息","Annual payments of dividends="],
        ["次，到期年数",", Maturity(years)="],
        ["，到期收益率",", YTM="],
        ['到期时间(年)','Maturity(years)'],
        ['债券价格变化','Change of bond price'],
        ["债券价格的变化与到期时间的关系","Changes of Bond Price vs Maturity"],
        ["债券价格的变化","Change of bond price"],
        ["次，期限",", Maturity="],
        ["年"," years"],
        ["债券价格的变化速度","Speed of bond price change"],
        
        ["债券到期时间与债券价格的变化速度","Speed of Bond Price Change vs Maturity"],
        ["收益率下降导致的债券价格增加","Bond price rises by falling YTM"],
        ["收益率上升导致的债券价格下降","Bond price falls by rising YTM"],
        ["收益率上升导致的债券价格下降(两次翻折后)","Bond price falls by rising YTM(folding up twice)"],
        ["到期收益率与债券价格变化的非对称性","Asymmetry of Bond Price Change vs YTM"],
        ["到期收益率及其变化幅度","到期收益率及其变化幅度"],
        ["数据来源：中债登/中国债券信息网，","数据来源：中债登/中国债券信息网，"],
        ['中国债券信息网','中国债券信息网'],
        ["中国债券价格指数走势","中国债券价格指数走势"],
        ["到期期限对债券转换因子的影响","到期期限对债券转换因子的影响"],
        ["名义券利率         :","名义券利率         :"],
        ["债券票面利率       :","债券票面利率       :"],
        ["每年付息次数       :","每年付息次数       :"],
        ["到下个付息日的天数 :","到下个付息日的天数 :"],
        ['债券到期期限*','债券到期期限*'],
        ['转换因子','转换因子'],
        
        ["*指下一付息日后剩余的付息次数","*指下一付息日后剩余的付息次数"],
        ['债券的转换因子','债券的转换因子'],
        ["到期期限对债券转换因子的影响","到期期限对债券转换因子的影响"],
        ['下一付息日后剩余的付息次数','下一付息日后剩余的付息次数'],
        ["【债券描述】名义券利率：","【债券描述】名义券利率："],
        [", 债券票面利率：",", 债券票面利率："],
        [', 每年付息次数：',', 每年付息次数：'],
        ["到下一付息日的天数：","到下一付息日的天数："],
        ["债券票息率对转换因子的影响","债券票息率对转换因子的影响"],
        ["名义券利率                 :","名义券利率                 :"],
        ["每年付息次数               :","每年付息次数               :"],
        ["到下个付息日的天数         :","到下个付息日的天数         :"],
        ["下个付息日后剩余的付息次数 :","下个付息日后剩余的付息次数 :"],
        ['债券票息率','债券票息率'],
        ["债券票息率对转换因子的影响","债券票息率对转换因子的影响"],
        ['票息率','票息率'],
        ["下一付息日后剩余的付息次数：","下一付息日后剩余的付息次数："],
        ["债券票息率与债券价格变化风险的关系","Risk of Bond Price Change vs Coupon Rate"],
        ["票息率及其变化幅度","Coupon rate and changes"],
        ["债券面值","债券面值"],
        
        ["，票面利率","，票面利率"],
        ["每年付息","每年付息"],
        ["次，期限","次，期限"],
        ["，到期收益率","，到期收益率"],
        
        ["======= 中国公募基金种类概况 =======","======= 中国公募基金种类概况 ======="],
        ["公募基金总数：","公募基金总数："],
        ["其中包括：","其中包括："],
        ["数据来源：东方财富/天天基金,","数据来源：东方财富/天天基金,"],
        ["\n===== 中国开放式基金排名：单位净值最高前十名 =====","\n===== 中国开放式基金排名：单位净值最高前十名 ====="],
        ["\n===== 中国开放式基金排名：累计净值最高前十名 =====","\n===== 中国开放式基金排名：累计净值最高前十名 ====="],
        ["\n===== 中国开放式基金排名：手续费最高前十名 =====","\n===== 中国开放式基金排名：手续费最高前十名 ====="],
        ["共找到披露净值信息的开放式基金数量:","共找到披露净值信息的开放式基金数量:"],
        ["基金类型:","基金类型:"],
        ["  净值日期:","  净值日期:"],
        ['单位净值','单位净值'],
        ['累计净值','累计净值'],
        ['净值','净值'],
        ["开放式基金的净值趋势：","开放式基金的净值趋势："],
        ['累计收益率%','累计收益率%'],
        ['收益率%','收益率%'],
        ["开放式基金的累计收益率趋势：","开放式基金的累计收益率趋势："],
        ['同类排名','同类排名'],
        ['同类排名百分比','同类排名百分比'],
        ["开放式基金的近三个月收益率排名趋势：","开放式基金的近三个月收益率排名趋势："],
        ['开放式基金总排名','开放式基金总排名'],
        ["\n======= 中国货币型基金排名：7日年化收益率最高前十名 =======","\n======= 中国货币型基金排名：7日年化收益率最高前十名 ======="],
        ["共找到披露收益率信息的货币型基金数量:","共找到披露收益率信息的货币型基金数量:"],
        ["收益率日期:","收益率日期:"],
        ['7日年化%','7日年化%'],
        ["货币型基金的7日年化收益率趋势：","货币型基金的7日年化收益率趋势："],
        ["\n===== 中国ETF基金排名：单位净值最高前十名 =====","\n===== 中国ETF基金排名：单位净值最高前十名 ====="],
        ["\n===== 中国ETF基金排名：累计净值最高前十名 =====","\n===== 中国ETF基金排名：累计净值最高前十名 ====="],
        ["\n===== 中国开放式基金排名：市价最高前十名 =====","\n===== 中国开放式基金排名：市价最高前十名 ====="],
        ["共找到披露净值信息的ETF基金数量:","共找到披露净值信息的ETF基金数量:"],
        ["基金类型:","基金类型:"],
        
        ["  净值日期:","  净值日期:"],
        ["  数据来源：东方财富/天天基金,","  数据来源：东方财富/天天基金,"],
        ['人民币元','人民币元'],
        ["ETF基金的净值趋势：","ETF基金的净值趋势："],
        ["\n===== 中国基金投资机构概况 =====","\n===== 中国基金投资机构概况 ====="],
        ["机构（会员）数量：","机构（会员）数量："],
        ["其中包括：","其中包括："],
        ["数据来源：中国证券投资基金业协会","数据来源：中国证券投资基金业协会"],
        ["\n===== 中国基金投资机构会员代表概况 =====","\n===== 中国基金投资机构会员代表概况 ====="],
        ["会员代表人数：","会员代表人数："],
        ["其中工作在：","其中工作在："],
        ["\n===== 中国私募基金管理人角色分布 =====","\n===== 中国私募基金管理人角色分布 ====="],
        ["地域：","地域："],
        ["法定代表人/执行合伙人数量：","法定代表人/执行合伙人数量："],
        ['\b, 占比全国','\b, 占比全国'],
        ["其中, 角色分布：","其中, 角色分布："],
        ["\n== 中国私募基金管理人地域分布概况 ==","\n== 中国私募基金管理人地域分布概况 =="],
        ["其中分布在：","其中分布在："],
        ["上述地区总计占比:","上述地区总计占比:"],
        ["\n== 中国私募基金管理人的产品与运营概况 ==","\n== 中国私募基金管理人的产品与运营概况 =="],
        ["产品数量：","产品数量："],
        ["产品的运营方式分布：","产品的运营方式分布："],
        ["产品的运营状态分布：","产品的运营状态分布："],
        ["\n===== 中国推出产品数量最多的私募基金管理人 =====","\n===== 中国推出产品数量最多的私募基金管理人 ====="],
        ["上述产品总计占比:","上述产品总计占比:"],
        ["\n===== 中国私募基金管理人的产品托管概况 =====","\n===== 中国私募基金管理人的产品托管概况 ====="],
        ["上述金融机构托管产品总计占比:","上述金融机构托管产品总计占比:"],
        ["\n===== 股票分红历史 =====","\n===== Stock Dividend History ====="],
        ["\n===== 股票分拆历史 =====","\n===== Stock Split History ====="],
        ["\n===== 投资组合的可持续发展风险 =====","\n===== 投资组合的可持续发展风险 ====="],
        
        ["总貌","Overall"],["主板","Main board"],["科创板","STAR board"],["创业板","GEM board"],
        ["上市股票/只","Number of stocks"],
        ["总股本/亿股（份）","Total shares(100m)"],["总股本/亿股","Total shares(100m)"],
        ["流通股本/亿股（份）","Shares outstanding(100m)"],["流通股本/亿股","Shares outstanding(100m)"],
        ["总市值/亿元","Total value(RMB 100m)"],
        ["流通市值/亿元","Total value outstanding(RMB 100m)"],
        
        ["企业横向对比: 业绩快照（TTM）","Comparing Companies: Performance Snapshot"],
        ["数据来源: 雅虎财经, ","Source: Yahoo Finance, "],
        [": 基于年(季)报的业绩历史对比",': Performance by Annual/Quarterly Reports'],
        ["企业横向对比: 实际税负",'Comparing Companies: Actual Tax Burden'],
        ["===== 杜邦分析分项数据表 =====","===== Du Pont Identity Items ====="],
        ["杜邦分析对比图","Comparing Companies: Du Pont Identity"],
        ["【图示放大比例】","[Legend amplifier]"],
        ['【财报日期及类型】',"[Date & type of report]"],
        ["杜邦分析分解项目","Items"],["季报","Quarterly"],["年报","Annual"],
        
        ['投资组合：马科维茨有效边界',"Investment Portfolio: Markowitz Efficient Frontier"],
        ['预期风险',"Expected risk"],["预期收益","Expected return"],
        ['投资组合由',"Portfolio includes "],['观察期：',"Watch period: "],
        ['有效边界',"Efficient frontier"],['无效边界',"Inefficient frontier"],
        ['风险最低点',"Lowest risk point"],['风险最低点',"Lowest risk point"],
        ['投资组合: 马科维茨可行集的夏普比率分布',"Markowitz Efficient Set: Distribution of Sharpe Ratio"],
        ["投资组合: MSR点和GMV点的位置","Investment Portfolio: MSR & GMV Points"],
        ["投资组合: 累计收益率的比较","Investment Portfolio: Comparison of Cumulative Return"],
        ["累计收益率","Cumulative Return"],["成分股：","Stocks:"],
        ["投资组合的构造方式: 最高夏普比率(MSR)","Portfolio Strategy: Max Sharpe Ratio(MSR)"],
        ["权重：","Weights of shares:"],
        ["投资组合的构造方式: 风险最小化(GMV)","Portfolio Strategy: Global Minimum Variance(GMV)"],
        ['投资组合',"Portfolio"],["日收益率%","Daily Return%"],
        ["投资组合: 日收益率的变化趋势","Portfolio: Daily Return Trend"],
        ["投资组合: 累计收益率的变化趋势","Portfolio: Cumulative Return Trend"],
        ["累计收益率","Cumulative Return"],
        ["投资组合: 累计收益率的比较","Portfolio: Cumulative Return Comparison"],
        ["投资组合: 马科维茨可行集","Investment Portfolio: Markowitz Efficient Set"],
        ["投资组合: 成分股收益率之间的相关系数","Correlation among Stock Returns"],
        ["投资组合: 成分股收益率之间的相关系数","Correlation Coefficients of Stock Returns"],
        ["股票","Stock"],
        
        
        ], columns=['code','codename'])

    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译文字，返回原文
        codename=code
   
    return codename

if __name__=='__main__':
    code='数据来源：雅虎财经，'
    print(texttranslate(code))

#==============================================================================


def tickertranslate(code):
    """
    套壳函数
    输入：证券代码。输出：证券名称
    """
    codename=codetranslate(code)
    return codename

if __name__=='__main__':
    code='GOOG'
    print(tickertranslate('000002.SZ'))
    print(tickertranslate('9988.HK'))

#==============================================================================
#==============================================================================
