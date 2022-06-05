import pytest
import QuantLib as ql
from exotx.data.marketdata import MarketData
from exotx.instruments.autocallable import Autocallable
from exotx.models.hestonmodel import HestonModel


# Arrange
@pytest.fixture
def my_reference_date():
    return ql.Date(6, 11, 2015)


@pytest.fixture
def my_market_data():
    day_count = ql.Actual365Fixed()
    reference_date = ql.Date(6, 11, 2015)
    spot = 100.0
    black_scholes_volatility = 0.2
    risk_free_rate = 0.01
    dividend_rate = 0.0
    yield_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(reference_date, risk_free_rate, day_count))
    dividend_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(reference_date, dividend_rate, day_count))

    return MarketData(reference_date=reference_date,
                      spot=spot,
                      yield_ts=yield_ts,
                      dividend_ts=dividend_ts,
                      black_scholes_volatility=black_scholes_volatility)


@pytest.fixture
def my_autocallable():
    notional = 100
    strike = 100
    autocall_barrier_level = 1.0
    coupon = 0.03
    coupon_barrier_level = 0.75
    protection_barrier_level = 0.75

    return Autocallable(notional, strike, autocall_barrier_level, coupon, coupon_barrier_level, protection_barrier_level)


def test_autocallable_black_scholes_price(my_autocallable: Autocallable,
                                          my_reference_date: ql.Date,
                                          my_market_data: MarketData):
    # Act
    seed = 125
    model = 'black-scholes'
    pv = my_autocallable.price(my_reference_date, my_market_data, model, seed)

    # Assert
    assert pv == pytest.approx(96.1609093840671, abs=1e-10)
