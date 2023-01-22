import json
import QuantLib as ql
from datetime import datetime
from typing import List, Union
from marshmallow import Schema, fields, post_load


class MarketData:

    def __init__(self,
                 spot: float,
                 risk_free_rate: float,
                 dividend_rate: float,
                 reference_date: Union[datetime, str, None] = None,
                 expiration_dates: List[Union[datetime, str]] = None,
                 strikes: List[float] = None,
                 data: List[List[float]] = None,
                 black_scholes_volatility: float = None) -> None:
        # set the reference date
        self._set_reference_date(reference_date)

        # set the underlying spot value
        self._set_underlying_spot(spot)

        # set market rate curves
        self._set_rate_curves(dividend_rate, risk_free_rate)

        # set the volatility surface
        self._set_volatility_surface(black_scholes_volatility, data, expiration_dates, strikes)

    # TODO: Have a proper rate curves stripper service
    def _set_rate_curves(self, dividend_rate, risk_free_rate):
        self.risk_free_rate = risk_free_rate
        self.dividend_rate = dividend_rate

    # TODO: Allow for multiple volatility surfaces for each underlying
    def _set_volatility_surface(self, black_scholes_volatility, data, expiration_dates, strikes):
        self.expiration_dates: List[datetime] = []
        if not expiration_dates:
            self.expiration_dates = None
        else:
            for expiration_date in expiration_dates:
                if isinstance(expiration_date, str):
                    self.expiration_dates.append(datetime.strptime(expiration_date, '%Y-%m-%d'))
                elif isinstance(expiration_date, datetime):
                    self.expiration_dates.append(expiration_date)
        self.strikes = strikes
        self.data = data
        self.black_scholes_volatility = black_scholes_volatility

    # TODO: Allow for multiple underlying spots to be defined, may need a proper container class
    def _set_underlying_spot(self, spot):
        assert spot > 0
        self.spot = spot

    def _set_reference_date(self, reference_date: Union[datetime, str, None]):
        if isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
        elif isinstance(reference_date, datetime):
            pass
        else:
            # defaults to today's date
            reference_date = datetime.today()
        self.reference_date: datetime = reference_date

    def get_ql_reference_date(self) -> ql.Date:
        return ql.Date().from_date(self.reference_date)

    # TODO: Get these from a proper rate curve stripper service
    def get_yield_curve(self, day_counter) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.get_ql_reference_date(), self.risk_free_rate, day_counter)
        return ql.YieldTermStructureHandle(flat_forward)

    def get_dividend_curve(self, day_counter) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.get_ql_reference_date(), self.dividend_rate, day_counter)
        return ql.YieldTermStructureHandle(flat_forward)

    @classmethod
    def from_json(cls, data: dict):
        schema = MarketDataSchema()
        return schema.load(data)

    def to_json(self, format_type: str = "dict"):
        schema = MarketDataSchema()
        my_json = schema.dump(self)
        if format_type == "dict":
            return my_json
        elif format_type == "str":
            return json.dumps(my_json)
        else:
            raise NotImplemented(f"Invalid format type {format_type} when dumping")


# region Schema

class MarketDataSchema(Schema):
    spot = fields.Float(required=True)
    risk_free_rate = fields.Float(required=True)
    dividend_rate = fields.Float(required=True)
    reference_date = fields.DateTime(format='%Y-%m-%d', allow_none=True)
    expiration_dates = fields.List(fields.DateTime(format='%Y-%m-%d'), allow_none=True)
    strikes = fields.List(fields.Float(), allow_none=True)
    data = fields.List(fields.List(fields.Float), allow_none=True)
    black_scholes_volatility = fields.Float(allow_none=True)

    @post_load
    def make_market_data(self, data, **kwargs) -> MarketData:
        return MarketData(**data)

# endregion
