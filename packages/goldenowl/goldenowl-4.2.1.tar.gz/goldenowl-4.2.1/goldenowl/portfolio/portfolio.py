import itertools
import pandas as pd
import datetime as dt
from xirr.math import xirr
import goldenowl.asset.asset as at
import goldenowl.portfolio.holding as hd
from goldenowl.portfolio.simplePut import SimplePut

class Portfolio:
    def __init__(self, aName, aAssetRatioList):
        self.m_name = aName;
        self.m_holdingMap={asset.getName(): hd.Holding(asset.getName(), asset) for asset, ratio in aAssetRatioList};
        self.m_assetRatioMap={asset.getName(): ratio for asset, ratio in aAssetRatioList}
        self.m_cashFlow = {};
        self.m_hedge_det = ();

    def getHedgeDet(self):
        return self.m_hedge_det;

    def setLongPutHedge(self, aAsset, aBufferFraction, aHedgePortfolioRatio, aDuration, aDate):
        norm_date = pd.to_datetime(aDate);
        self.m_hedge_det = (aAsset, aBufferFraction, aDuration, aDate);
        hedge_hldng = SimplePut('__Hedge__',aAsset, aAsset.getValue(aDate)*(1-aBufferFraction), norm_date+aDuration, aHedgePortfolioRatio); 
        correction_ratio = 1;
        if ('__Hedge__' in self.m_assetRatioMap):
            self.rebalance(aDate);
            correction_ratio = (1-aHedgePortfolioRatio)/(1-self.m_assetRatioMap['__Hedge__']);
        else:
            correction_ratio = 1-aHedgePortfolioRatio;

        for ast, ratio in self.m_assetRatioMap.items():
            self.m_assetRatioMap[ast] = correction_ratio * ratio;
        self.m_holdingMap['__Hedge__'] = hedge_hldng;
        self.m_assetRatioMap['__Hedge__'] = aHedgePortfolioRatio;
        tot_ratio =0;
        for ast, ratio in self.m_assetRatioMap.items():
            tot_ratio+= ratio;
        assert(tot_ratio == 1);



    def rebalance(self, aDate):
        tot_amount = 0;
        norm_date = pd.to_datetime(aDate);
        for a, hld in self.m_holdingMap.items():
            tot_amount += hld.getValue(aDate);

        if (tot_amount == 0):
            return;

        cur_ratio = {ast: hold.getValue(aDate)/tot_amount for ast, hold in self.m_holdingMap.items() };
        adj_ratio = {key: val - cur_ratio[key] for key, val in self.m_assetRatioMap.items() };
        for astName, hldObj in self.m_holdingMap.items():
            ratio = adj_ratio[astName];
            if ratio > 0:
                hldObj.buyAmount(tot_amount*ratio, aDate);
                self.m_cashFlow[norm_date] = tot_amount*ratio;
            else:
                hldObj.sellAmount(-1*tot_amount*ratio, aDate);
                self.m_cashFlow[norm_date] = tot_amount*ratio;


    def addAmount(self, aAmount, aDate):
        norm_date = pd.to_datetime(aDate);
        for asset, ratio in self.m_assetRatioMap.items():
            self.m_holdingMap[asset].buyAmount(aAmount * ratio, aDate);
        self.m_cashFlow[norm_date] = aAmount;

    def removeAmount(self, aAmount, aDate):
        norm_date = pd.to_datetime(aDate);
        for asset, ratio in self.m_assetRatioMap.items():
            self.m_holdingMap[asset].sellAmount(aAmount * ratio, aDate);
        self.m_cashFlow[norm_date] = -aAmount;

    def getValue(self, aDate):
        value = 0;
        for asset, holding in self.m_holdingMap.items():
            value += holding.getValue(aDate);
        return value;
    
    def getXIRR(self, aDate):
        norm_date = pd.to_datetime(aDate);
        cash_flow =self.m_cashFlow;
        filtered = dict(itertools.filterfalse(lambda i:i[0] > norm_date, cash_flow.items()))
        final_val = self.getValue(aDate);
        if (norm_date in filtered.keys()):
            filtered[norm_date]-= final_val;
        else:
            filtered[norm_date]= -final_val;
        return xirr(filtered)


#Free floating functions below

def getSIPReturn(aInstrRatioList, aSipFreq, aRebalanceFreq, aStart, aEnd,
                 aHedgeAsset=None, aHedgeBufferFraction= None, aHedgeDuration=None, aHedgePortfolioRatio=None):
    prtf = Portfolio('Calc', aInstrRatioList);
    norm_date = pd.to_datetime(aStart);
    if (aHedgeAsset != None):
        prtf.setLongPutHedge(aHedgeAsset, aHedgeBufferFraction, aHedgePortfolioRatio, aHedgeDuration, norm_date);

    norm_end_date = pd.to_datetime(aEnd);
    sip_date = norm_date;
    rebal_date = norm_date;

    while(sip_date < norm_end_date):
        prtf.addAmount(100, sip_date);
        sip_date+=dt.timedelta(days=aSipFreq);

    while(rebal_date < norm_end_date):
        prtf.rebalance(rebal_date);
        if (aHedgeAsset != None):
            cur_hedge_det = prtf.getHedgeDet();
            cur_hedge_level = cur_hedge_det[0].getValue(cur_hedge_det[3]) * (1-cur_hedge_det[1]);
            new_hedge_level =aHedgeAsset.getValue(rebal_date) * (1 - aHedgeBufferFraction);
            if ((new_hedge_level > cur_hedge_level) or cur_hedge_det[3]+cur_hedge_det[2] < rebal_date): 
                prtf.setLongPutHedge(aHedgeAsset, aHedgeBufferFraction, aHedgePortfolioRatio, aHedgeDuration, rebal_date);
        rebal_date+=dt.timedelta(days=aRebalanceFreq);

    return prtf.getXIRR(norm_end_date);

