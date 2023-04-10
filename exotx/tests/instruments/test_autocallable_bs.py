import pytest

from exotx import price
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.instruments.autocallable import Autocallable


# Arrange
@pytest.fixture
def my_market_data() -> MarketData:
    reference_date = '2015-11-06'
    underlying_spots = [100.0]
    underlying_black_scholes_volatilities = [0.2]
    risk_free_rate = 0.01
    dividend_rate = 0.0

    return MarketData(reference_date=reference_date,
                      underlying_spots=underlying_spots,
                      risk_free_rate=risk_free_rate,
                      dividend_rate=dividend_rate,
                      underlying_black_scholes_volatilities=underlying_black_scholes_volatilities)


@pytest.fixture
def my_autocallable() -> Autocallable:
    notional = 100
    strike = 100
    autocall_barrier_level = 1.0
    coupon = 0.03
    coupon_barrier_level = 0.75
    protection_barrier_level = 0.75

    return Autocallable(notional, strike, autocall_barrier_level, coupon, coupon_barrier_level,
                        protection_barrier_level)


def test_autocallable_black_scholes_price(my_autocallable: Autocallable,
                                          my_market_data: MarketData,
                                          my_static_data: StaticData) -> None:
    # Act
    seed = 125
    model = 'black-scholes'
    pv = price(my_autocallable, my_market_data, my_static_data, model, seed)

    # Assert
    assert pv == pytest.approx(96.08517973497098, abs=1e-10)
