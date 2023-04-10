import json
from datetime import datetime
from typing import List, Union

import QuantLib as ql
from marshmallow import Schema, fields, post_load


class MarketData:

    def __init__(self,
                 underlying_spots: List[float],
                 risk_free_rate: float,
                 dividend_rate: float,
                 reference_date: Union[datetime, str, None] = None,
                 expiration_dates: List[Union[datetime, str]] = None,
                 strikes: List[float] = None,
                 data: List[List[float]] = None,
                 underlying_black_scholes_volatilities: List[float] = None,
                 correlation_matrix: List[List[float]] = None) -> None:
        # set the reference date
        self._set_reference_date(reference_date)

        # set underlying spot values
        self._set_underlying_spots(underlying_spots)

        # set market rate curves
        self._set_rate_curves(dividend_rate, risk_free_rate)

        # set the volatility surface
        self._set_volatility_surface(underlying_black_scholes_volatilities, data, expiration_dates, strikes)

        # set the correlation matrix
        self._set_correlation_matrix(correlation_matrix)

    # region setters

    # TODO: Have a proper rate curves stripper service
    def _set_rate_curves(self, dividend_rate, risk_free_rate) -> None:
        self.risk_free_rate = risk_free_rate
        self.dividend_rate = dividend_rate

    # TODO: Allow for multiple volatility surfaces for each underlying
    def _set_volatility_surface(self, underlying_black_scholes_volatilities: List[float], data, expiration_dates,
                                strikes) -> None:
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

        if underlying_black_scholes_volatilities:
            for vol in underlying_black_scholes_volatilities:
                assert vol >= 0, f"Invalid volatility: {vol}"
        self.underlying_black_scholes_volatilities = underlying_black_scholes_volatilities  # set to None if it does not exist, OK

    # TODO: Allow for multiple underlying spots to be defined, may need a proper container class or a dict
    def _set_underlying_spots(self, underlying_spots: List[float]) -> None:
        for underlying_spot in underlying_spots:
            assert underlying_spot > 0, f"Invalid underlying spot {underlying_spot}"
        self.underlying_spots = underlying_spots

    def _set_reference_date(self, reference_date: Union[datetime, str, None]) -> None:
        if isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
        elif isinstance(reference_date, datetime):
            pass
        else:
            # defaults to today's date
            reference_date = datetime.today()
        self.reference_date: datetime = reference_date

    def _set_correlation_matrix(self, correlation_matrix: Union[List[List[float]], None]) -> None:
        if correlation_matrix:
            for rows in correlation_matrix:
                for rho in rows:
                    assert 1 >= rho >= -1, "Invalid correlation matrix"
        self.correlation_matrix = correlation_matrix

    # endregion

    # region getters
    def get_ql_reference_date(self) -> ql.Date:
        return ql.Date().from_date(self.reference_date)

    def get_correlation_matrix(self) -> ql.Matrix:
        matrix = ql.Matrix(len(self.correlation_matrix), len(self.correlation_matrix))
        for i in range(len(self.correlation_matrix)):
            matrix[i][i] = 1.0
            for j in range(i + 1, len(self.correlation_matrix)):
                matrix[i][j] = self.correlation_matrix[i][j]
                matrix[j][i] = self.correlation_matrix[i][j]
        return matrix

    # TODO: Get these from a proper rate curve stripper service
    def get_yield_curve(self, day_counter) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.get_ql_reference_date(), self.risk_free_rate, day_counter)
        return ql.YieldTermStructureHandle(flat_forward)

    def get_dividend_curve(self, day_counter) -> ql.YieldTermStructureHandle:
        flat_forward = ql.FlatForward(self.get_ql_reference_date(), self.dividend_rate, day_counter)
        return ql.YieldTermStructureHandle(flat_forward)

    # endregion

    # region serialization/deserialization
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
            raise NotImplementedError(f"Invalid format type {format_type} when dumping")
    # endregion


# region Schema

class MarketDataSchema(Schema):
    underlying_spots = fields.List(fields.Float(required=True))
    risk_free_rate = fields.Float(required=True)
    dividend_rate = fields.Float(required=True)
    reference_date = fields.DateTime(format='%Y-%m-%d', allow_none=True)
    expiration_dates = fields.List(fields.DateTime(format='%Y-%m-%d'), allow_none=True)
    strikes = fields.List(fields.Float(), allow_none=True)
    data = fields.List(fields.List(fields.Float), allow_none=True)
    underlying_black_scholes_volatilities = fields.List(fields.Float(allow_none=True))
    correlation_matrix = fields.List(fields.List(fields.Float()))

    @post_load
    def make_market_data(self, data, **kwargs) -> MarketData:
        return MarketData(**data)

# endregion
