from .dll import jpmcds
import pandas as pd
import numpy as np
from .dll.jpmcds import list2vector,date2str



class discountCurve(jpmcds.discountCurve):

    def __init__(self, 
        expiries=["1M","2M","3M","6M","9M","1Y","2Y","3Y","4Y","5Y","6Y","7Y","8Y","9Y","10Y","12Y","15Y","20Y","25Y","30Y"],
        rates = [0.2463, 0.2575, 0.2919, 0.6794, 1.0069, 1.2913, 1.2986, 1.9202, 2.3933, 2.7456, 3.0167, 3.2234, 3.3788, 3.4960, 3.5935, 3.7503, 3.9021,3.9970, 4.0394, 4.0619],
        types = "MMMMMSSSSSSSSSSSSSSS"
        ):
        rates = (np.array(rates)/100).tolist()
        daycounter1 = "30/360"
        daycounter2 = "Act/360"
        payfreq = "6M"
        baseDate = "2009/9/22"
        expiries = list2vector(expiries, str())
        rates = list2vector(rates, float())
        
        jpmcds.discountCurve.__init__(self, daycounter1, daycounter2, payfreq, baseDate, expiries, rates, types)
        #jpmcds.discountCurve.__init__(self)
        
        
    def build(self):
        jpmcds.discountCurve.build(self)
        return self

    def printer(self):
        icurve = jpmcds.discountCurve.print(self)
        zc = pd.DataFrame(date2str(icurve.date), columns=["date"])
        zc["rate"] = icurve.rate
        return zc

class spreadCurve(jpmcds.spreadcurve):
    def __init__(self,
        expiries = ["6M","1Y","2Y","3Y","4Y","5Y","7Y","10Y"],
        couponRates = [0.0012, 0.0015, 0.0021, 0.0027, 0.0032, 0.0036, 0.0056, 0.0070],
        baseDate = "2009/9/20",
        daycounter = "Act/360",
        payfreq = "1S",
        ):
        expiries = list2vector(expiries, str())
        couponRates = list2vector(couponRates, float())
        jpmcds.spreadcurve.__init__(self, daycounter, payfreq, baseDate, expiries, couponRates)

    def build(self, objDiscCurve):
        jpmcds.spreadcurve.build(self, objDiscCurve)
        return self
    
    def printer(self):
        icurve = jpmcds.spreadcurve.print(self)
        zc = pd.DataFrame(date2str(icurve.date), columns=["date"])
        zc["rate"] = icurve.rate
        return zc


class CDS(jpmcds.cds):
    def __init__(self,
        today = "2009/9/18",
        settleDate = "2009/9/18",
        stepinDate = "2009/9/18",
        startDate = "2009/6/22",
        endDate = "2014/9/20",
        notional = 1000000,
        couponRate = 0.0036,
        recoveryRate = 0.4,
        daycounter = "Act/360",
        payfreq = "1S",
        stubType = "f/s",
        payAccOnDefault = False,
        protectStart = True,
        protectPayOnMat = True
        ):
        jpmcds.cds.__init__(self,today, settleDate, stepinDate, startDate, endDate, notional, couponRate, 
                recoveryRate, daycounter, payfreq, stubType, payAccOnDefault, protectStart, protectPayOnMat)

    
    def pricing(self, objDiscCurve, objSpreadCurve):
        jpmcds.cds.Pricing(self, objDiscCurve, objSpreadCurve)
        return self
    
    def feeLegFlow(self):
        clsfl = jpmcds.cds.feeLegFlow(self)
        fl = pd.DataFrame(date2str(clsfl.accStartD), columns=["accStart"])
        fl["accEnd"] = date2str(clsfl.accEndD)
        fl["accTime"] = clsfl.accTime
        fl["payD"] = date2str(clsfl.payD)
        fl["amount"] = clsfl.amount
        return fl
    
    def contLegFlow(self):
        clscl = jpmcds.cds.contLegFlow(self)
        cl = pd.DataFrame(date2str(clscl.date_d), columns=["date_d"])
        cl["date_s"] = date2str(clscl.date_s)
        cl["survival"] = clscl.survival
        cl["discount"] = clscl.discount
        cl.loc[1:,"accrual"] = clscl.accrual
        return cl




if __name__ == "__main__":
    pd.set_option('display.max_rows',500)

    curve1 = discountCurve().build()
    curve1.printer()
    
    curve2 = spreadCurve().build(curve1)
    
    cds1 = CDS().pricing(curve1, curve2)
    
    


    


