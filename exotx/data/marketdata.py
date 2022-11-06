import QuantLib as ql
from datetime import datetime
from typing import List, Union


class MarketData(object):

    def __init__(self,
                 reference_date: Union[datetime, str],
                 spot: float,
                 risk_free_rate: float,
                 dividend_rate: float,
                 expiration_dates: List[Union[datetime, str]] = None,
                 strikes: List[float] = None,
                 data: List[List[float]] = None,
                 black_scholes_volatility: float = None) -> None:
        # set the reference date
        if isinstance(reference_date, str):
            reference_date = ql.Date().from_date(datetime.strptime(reference_date, "%Y-%m-%d"))
        elif isinstance(reference_date, datetime):
            reference_date = ql.Date().from_date(reference_date)
        else:
            # defaults to today's date
            reference_date = ql.Date_todaysDate()
        self.reference_date = reference_date

        # set the spot underlying value
        assert spot > 0
        self.spot = spot

        # TODO: define this in a StaticData object instead
        # set day counter
        self.day_counter = ql.Actual360()

        # set market rate curves
        self.risk_free_rate = risk_free_rate
        self.dividend_rate = dividend_rate

        # set the volatility surface
        self.expiration_dates: List[datetime] = []
        if not expiration_dates:
            self.expiration_dates = None
        else:
            for expiration_date in expiration_dates:
                if isinstance(expiration_date, str):
                    self.expiration_dates.append(datetime.strptime(expiration_date, "%Y-%m-%d"))
                elif isinstance(expiration_date, datetime):
                    self.expiration_dates.append(expiration_date)
        self.strikes = strikes
        self.data = data
        self.black_scholes_volatility = black_scholes_volatility

    def get_yield_curve(self) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.reference_date, self.risk_free_rate, self.day_counter)
        return ql.YieldTermStructureHandle(flat_forward)

    def get_dividend_curve(self) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.reference_date, self.dividend_rate, self.day_counter)
        return ql.YieldTermStructureHandle(flat_forward)
