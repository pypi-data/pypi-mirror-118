import itertools
import pandas as pd
import datetime as dt
from xirr.math import xirr
import goldenowl.asset.asset
from goldenowl.portfolio.holding import Holding

class SimplePut(Holding):
    def __init__(self, aName, aAsset, aStrike, aExpiry, aOTMCostFactor):
        Holding.__init__(self, aName, aAsset);
        self.m_otm_cost_factor = aOTMCostFactor;
        self.m_strike = aStrike;
        self.m_expiry = pd.to_datetime(aExpiry);


    def _getAssetValue(self, aDate):
        norm_date = pd.to_datetime(aDate);
        underlying_val = -1;
        if (norm_date < self.m_expiry):
            underlying_val = self.m_inst_pr_map.getValue(aDate);
            prem_val = self.m_otm_cost_factor*underlying_val;
            if (underlying_val < self.m_strike):
                return prem_val + self.m_strike - underlying_val;
            else:
                return prem_val;
        else:
            underlying_val = self.m_inst_pr_map.getValue(self.m_expiry);
            if (underlying_val < self.m_strike):
                return self.m_strike - underlying_val;
            else:
                return 0;


