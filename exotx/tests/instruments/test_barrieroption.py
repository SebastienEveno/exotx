import pytest
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.instruments.barrieroption import BarrierOption, BarrierType


# replicates the tests in https://github.com/lballabio/QuantLib/blob/master/test-suite/barrieroption.cpp


# Arrange
@pytest.fixture
def my_barrier_option() -> BarrierOption:
    barrier_type = 'upandin'
    barrier = 105
    strike = 90
    maturity = '2016-05-04'  # time to maturity = 0.5
    exercise = 'european'
    option_type = 'call'
    rebate = 3.0

    return BarrierOption(barrier_type, barrier, strike, maturity, exercise, option_type, rebate)


# replicates https://github.com/lballabio/QuantLib/blob/master/test-suite/barrieroption.cpp#L280-L282
@pytest.mark.parametrize('barrier_type, strike, model, expected', [
    (BarrierType.UPANDIN, 90, 'analytic', 14.111173119603055),
    (BarrierType.UPANDIN, 100, 'analytic', 8.448206354250173),
    (BarrierType.UPANDIN, 110, 'analytic', 4.590969266108855),
    (BarrierType.UPANDIN, 90, 'fd-bs-barrier', 14.113898622657395),
    (BarrierType.UPANDIN, 90, 'fd-heston-barrier', 15.806560344445511)
])
def test_barrier_option_analytic_barrier_engine(my_barrier_option: BarrierOption,
                                                strike: float,
                                                barrier_type: BarrierType,
                                                my_market_data: MarketData,
                                                my_static_data: StaticData,
                                                model: str,
                                                expected: float) -> None:
    # Arrange
    my_barrier_option.strike = strike
    my_barrier_option.barrier_type = barrier_type
    # Act
    pv = my_barrier_option.price(my_market_data, my_static_data, model)

    # Assert
    assert pv == pytest.approx(expected, abs=1e-8)


def test_barrier_option_fd_black_scholes_rebate_engine(my_barrier_option: BarrierOption,
                                                       my_market_data: MarketData,
                                                       my_static_data: StaticData) -> None:
    # Act
    model = 'fd-bs-rebate'
    pv = my_barrier_option.price(my_market_data, my_static_data, model)

    # Assert
    assert pv == pytest.approx(2.9568061345268424, abs=1e-10)


def test_barrier_option_fd_heston_barrier_engine_constant_vol(my_barrier_option: BarrierOption,
                                                              my_market_data: MarketData,
                                                              my_static_data: StaticData) -> None:
    # Act
    model = 'fd-heston-barrier'
    # test if we retrieve the same price as BS
    my_market_data.data = [[my_market_data.black_scholes_volatility] * len(i) for i in my_market_data.data]
    pv = my_barrier_option.price(my_market_data, my_static_data, model)

    # Assert
    assert pv == pytest.approx(14.114219673481117, abs=1e-8)
