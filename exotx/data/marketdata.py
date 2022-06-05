import QuantLib as ql
from typing import List


class MarketData(object):

    def __init__(self,
                 reference_date: ql.Date,
                 spot: float,
                 yield_ts: ql.YieldTermStructureHandle,
                 dividend_ts: ql.YieldTermStructureHandle,
                 expiration_dates: List[ql.Date] = None,
                 strikes: List[float] = None,
                 data: List[List[float]] = None,
                 black_scholes_volatility: float = None) -> None:
        self.reference_date = reference_date
        assert spot > 0
        self.spot = spot
        self.expiration_dates = expiration_dates
        self.strikes = strikes
        self.data = data  # volatility surface
        self.black_scholes_volatility = black_scholes_volatility
        self.yield_ts = yield_ts
        self.dividend_ts = dividend_ts
