import pytest
import QuantLib as ql
from datetime import datetime
from exotx.data.marketdata import MarketData
from exotx.instruments.autocallable import Autocallable


# Arrange
@pytest.fixture
def my_reference_date():
    return datetime(2015, 11, 6)


@pytest.fixture
def my_market_data():
    reference_date = datetime(2015, 11, 6)
    spot = 100.0
    risk_free_rate = 0.01
    dividend_rate = 0.0
    expiration_dates = [ql.Date(6, 12, 2015), ql.Date(6, 1, 2016), ql.Date(6, 2, 2016),
                        ql.Date(6, 3, 2016), ql.Date(6, 4, 2016), ql.Date(6, 5, 2016),
                        ql.Date(6, 6, 2016), ql.Date(6, 7, 2016), ql.Date(6, 8, 2016),
                        ql.Date(6, 9, 2016), ql.Date(6, 10, 2016), ql.Date(6, 11, 2016),
                        ql.Date(6, 12, 2016), ql.Date(6, 1, 2017), ql.Date(6, 2, 2017),
                        ql.Date(6, 3, 2017), ql.Date(6, 4, 2017), ql.Date(6, 5, 2017),
                        ql.Date(6, 6, 2017), ql.Date(6, 7, 2017), ql.Date(6, 8, 2017),
                        ql.Date(6, 9, 2017), ql.Date(6, 10, 2017), ql.Date(6, 11, 2017)]
    expiration_dates = [ql_date.to_date() for ql_date in expiration_dates]
    strikes = [70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0]
    data = [
        [0.37819, 0.34177, 0.30394, 0.27832, 0.26453, 0.25916, 0.25941, 0.26127],
        [0.3445, 0.31769, 0.2933, 0.27614, 0.26575, 0.25729, 0.25228, 0.25202],
        [0.37419, 0.35372, 0.33729, 0.32492, 0.31601, 0.30883, 0.30036, 0.29568],
        [0.37498, 0.35847, 0.34475, 0.33399, 0.32715, 0.31943, 0.31098, 0.30506],
        [0.35941, 0.34516, 0.33296, 0.32275, 0.31867, 0.30969, 0.30239, 0.29631],
        [0.35521, 0.34242, 0.33154, 0.3219, 0.31948, 0.31096, 0.30424, 0.2984],
        [0.35442, 0.34267, 0.33288, 0.32374, 0.32245, 0.31474, 0.30838, 0.30283],
        [0.35384, 0.34286, 0.33386, 0.32507, 0.3246, 0.31745, 0.31135, 0.306],
        [0.35338, 0.343, 0.33464, 0.32614, 0.3263, 0.31961, 0.31371, 0.30852],
        [0.35301, 0.34312, 0.33526, 0.32698, 0.32766, 0.32132, 0.31558, 0.31052],
        [0.35272, 0.34322, 0.33574, 0.32765, 0.32873, 0.32267, 0.31705, 0.31209],
        [0.35246, 0.3433, 0.33617, 0.32822, 0.32965, 0.32383, 0.31831, 0.31344],
        [0.35226, 0.34336, 0.33651, 0.32869, 0.3304, 0.32477, 0.31934, 0.31453],
        [0.35207, 0.34342, 0.33681, 0.32911, 0.33106, 0.32561, 0.32025, 0.3155],
        [0.35171, 0.34327, 0.33679, 0.32931, 0.3319, 0.32665, 0.32139, 0.31675],
        [0.35128, 0.343, 0.33658, 0.32937, 0.33276, 0.32769, 0.32255, 0.31802],
        [0.35086, 0.34274, 0.33637, 0.32943, 0.3336, 0.32872, 0.32368, 0.31927],
        [0.35049, 0.34252, 0.33618, 0.32948, 0.33432, 0.32959, 0.32465, 0.32034],
        [0.35016, 0.34231, 0.33602, 0.32953, 0.33498, 0.3304, 0.32554, 0.32132],
        [0.34986, 0.34213, 0.33587, 0.32957, 0.33556, 0.3311, 0.32631, 0.32217],
        [0.34959, 0.34196, 0.33573, 0.32961, 0.3361, 0.33176, 0.32704, 0.32296],
        [0.34934, 0.34181, 0.33561, 0.32964, 0.33658, 0.33235, 0.32769, 0.32368],
        [0.34912, 0.34167, 0.3355, 0.32967, 0.33701, 0.33288, 0.32827, 0.32432],
        [0.34891, 0.34154, 0.33539, 0.3297, 0.33742, 0.33337, 0.32881, 0.32492]]

    return MarketData(reference_date=reference_date,
                      spot=spot,
                      risk_free_rate=risk_free_rate,
                      dividend_rate=dividend_rate,
                      expiration_dates=expiration_dates,
                      strikes=strikes,
                      data=data)


@pytest.fixture
def my_autocallable():
    notional = 100
    strike = 100
    autocall_barrier_level = 1.0
    coupon = 0.03
    coupon_barrier_level = 0.75
    protection_barrier_level = 0.75

    return Autocallable(notional, strike, autocall_barrier_level, coupon, coupon_barrier_level, protection_barrier_level)


def test_autocallable_heston_price(my_autocallable: Autocallable,
                                   my_reference_date: datetime,
                                   my_market_data: MarketData):
    # Act
    seed = 125
    model = 'heston'
    pv = my_autocallable.price(my_reference_date, my_market_data, model, seed)

    # Assert
    assert pv == pytest.approx(101.97414577884945, abs=1e-10)
