import QuantLib as ql
from typing import Optional
from . import ql_enums as qle

def get_qlModel(model: qle.ShortRateModel,
                ts_handle: Optional[ql.QuantLib.YieldTermStructureHandle]=None,
                r0=0.05, 
                a=0.1, 
                b=0.05, 
                sigma=0.01, 
                lamda=0.0,
                eta=0.01, 
                rho=-0.75,
                volstepdates = None, 
                volatilities = None, 
                reversions = None):

    if model == qle.ShortRateModel.vasicek: 
        return ql.Vasicek(r0, a, b, sigma, lamda)
    elif model == qle.ShortRateModel.blackkarasinski:
        return ql.BlackKarasinski(ts_handle, a, sigma)
    elif model == qle.ShortRateModel.hullwhite:
        return ql.HullWhite(ts_handle, a, sigma)
    elif model == qle.ShortRateModel.gsr:
        return ql.Gsr(ts_handle, volstepdates, volatilities, reversions)
    elif model == qle.ShortRateModel.g2:
        return ql.G2(ts_handle, a, sigma, b, eta, rho) 
    else:
        return None


def qlShortRateModel(srmodel: qle.ShortRateModel,
                    yts_handle: ql.QuantLib.YieldTermStructureHandle,
                    **params):

    if srmodel == qle.ShortRateModel.vasicek: 
        return ql.Vasicek(params["r0"], params["a"], params["b"], params["sigma"], params["lamda"])
    elif srmodel == qle.ShortRateModel.blackkarasinski:
        return ql.BlackKarasinski(yts_handle, params["a"], params["sigma"])
    elif srmodel == qle.ShortRateModel.hullwhite:
        return ql.HullWhite(yts_handle, params["a"], params["sigma"])
    elif srmodel == qle.ShortRateModel.gsr:
        return ql.Gsr(yts_handle, params["volstepdates"], params["volatilities"], params["reversions"])
    elif srmodel == qle.ShortRateModel.g2:
        return ql.G2(yts_handle, params["a"], params["sigma"], params["b"], params["eta"], params["rho"]) 
    else:
        return None
    

def qlTreeCallableEngine(srmodel, gridpoints: int = 100):
    return ql.TreeCallableFixedRateBondEngine(srmodel, gridpoints)




