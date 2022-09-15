import QuantLib as ql
from datetime import datetime
from typing import List


class MarketData(object):

    def __init__(self,
                 reference_date: str,
                 spot: float,
                 risk_free_rate: float,
                 dividend_rate: float,
                 expiration_dates: List[datetime] = None,
                 strikes: List[float] = None,
                 data: List[List[float]] = None,
                 black_scholes_volatility: float = None) -> None:
        self.reference_date = ql.Date().from_date(datetime.strptime(reference_date, "%Y-%M-%d"))
        assert spot > 0
        self.spot = spot
        self.risk_free_rate = risk_free_rate
        self.dividend_rate = dividend_rate
        self.expiration_dates = expiration_dates
        self.strikes = strikes
        self.data = data  # volatility surface
        self.black_scholes_volatility = black_scholes_volatility

    def get_yield_curve(self) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.reference_date, self.risk_free_rate, ql.Actual365Fixed())
        return ql.YieldTermStructureHandle(flat_forward)

    def get_dividend_curve(self) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.reference_date, self.dividend_rate, ql.Actual365Fixed())
        return ql.YieldTermStructureHandle(flat_forward)
