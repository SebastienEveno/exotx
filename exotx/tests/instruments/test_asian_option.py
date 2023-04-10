from datetime import timedelta

import QuantLib as ql
import pytest

from exotx import price
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.instruments.asian_option import AsianOption, AverageCalculation, AverageConvention
from exotx.instruments.average_type import AverageType
from exotx.instruments.option_type import OptionType
from exotx.utils.pricing_configuration import PricingConfiguration


# Arrange
@pytest.fixture()
def my_static_data() -> StaticData:
    my_json = {
        'day_counter': 'Actual360',
        'business_day_convention': 'ModifiedFollowing'
    }
    return StaticData.from_json(my_json)


@pytest.fixture()
def my_market_data() -> MarketData:
    my_json = {
        'reference_date': '2015-11-06',
        'underlying_spots': [80],
        'risk_free_rate': 0.05,
        'dividend_rate': -0.03,
        'underlying_black_scholes_volatilities': [0.20]
    }

    return MarketData.from_json(my_json)


@pytest.fixture
def my_asian_option() -> AsianOption:
    strike = 85
    maturity = '2016-02-04'  # reference_date + 90 days
    exercise = 'european'
    option_type = OptionType.PUT
    # option_type = 'call'
    average_type = AverageType.GEOMETRIC
    # average_type = 'geometric'
    average_calculation = AverageCalculation.CONTINUOUS
    average_convention = AverageConvention.PRICE

    return AsianOption(strike, maturity, option_type, average_type, average_calculation, average_convention)


@pytest.fixture
def my_pricing_config() -> PricingConfiguration:
    model = PricingModel.BLACK_SCHOLES
    numerical_method = NumericalMethod.ANALYTIC

    return PricingConfiguration(model, numerical_method)


# Reproduces https://github.com/lballabio/QuantLib/blob/master/test-suite/asianoptions.cpp#L95
@pytest.mark.parametrize(
    'average_calculation, compute_greeks, expected_price, expected_delta, expected_gamma, expected_theta',
    [
        (AverageCalculation.CONTINUOUS, True, 4.6922, -0.80308771, 0.05935118, 0.05801764)
    ])
def test_price(my_asian_option: AsianOption,
               my_market_data: MarketData,
               my_static_data: StaticData,
               my_pricing_config: PricingConfiguration,
               average_calculation: AverageCalculation,
               compute_greeks: bool,
               expected_price: float,
               expected_delta: float,
               expected_gamma: float,
               expected_theta: float) -> None:
    # Arrange
    my_asian_option.average_calculation = average_calculation
    my_pricing_config.compute_greeks = compute_greeks

    # Act
    result = price(my_asian_option, my_market_data, my_static_data, my_pricing_config)

    # Assert
    assert result['price'] == pytest.approx(expected_price, abs=1e-4)
    if my_pricing_config.compute_greeks:
        assert result['delta'] == pytest.approx(expected_delta, abs=1e-8)
        assert result['gamma'] == pytest.approx(expected_gamma, abs=1e-8)
        assert result['theta'] == pytest.approx(expected_theta, abs=1e-8)


# Reproduces https://github.com/lballabio/QuantLib/blob/master/test-suite/asianoptions.cpp#L95
@pytest.mark.parametrize(
    'average_calculation, expected_price',
    [
        (AverageCalculation.DISCRETE, 4.6922)
    ])
def test_price_approximate_continuous_with_discrete_version(my_asian_option: AsianOption,
                                                            my_market_data: MarketData,
                                                            my_static_data: StaticData,
                                                            my_pricing_config: PricingConfiguration,
                                                            average_calculation: AverageCalculation,
                                                            expected_price: float) -> None:
    # Arrange
    my_asian_option.average_calculation = average_calculation
    my_asian_option.future_fixing_dates = [ql.Date().from_date(my_market_data.reference_date + timedelta(days=i))
                                           for i in range(1, 90)]

    # Act
    result = price(my_asian_option, my_market_data, my_static_data, my_pricing_config)

    # Assert
    assert result['price'] == pytest.approx(expected_price, abs=3.0e-3)


# Reproduces https://github.com/lballabio/QuantLib/blob/master/test-suite/asianoptions.cpp#L384
@pytest.mark.parametrize(
    'average_calculation, average_convention, strike, expected_price',
    [
        (AverageCalculation.DISCRETE, AverageConvention.STRIKE, 100, 4.97109)
    ])
def test_price_analytic_discrete_geometric_average_strike(my_asian_option: AsianOption,
                                                          my_market_data: MarketData,
                                                          my_static_data: StaticData,
                                                          my_pricing_config: PricingConfiguration,
                                                          average_calculation: AverageCalculation,
                                                          average_convention: AverageConvention,
                                                          strike: float,
                                                          expected_price: float) -> None:
    # Arrange
    my_asian_option.option_type = ql.Option.Call
    my_asian_option.maturity = ql.Date(31, 10, 2016)
    my_asian_option.strike = strike
    my_asian_option.average_calculation = average_calculation
    my_asian_option.future_fixing_dates = [ql.Date().from_date(my_market_data.reference_date + timedelta(days=36 * i))
                                           for i in range(1, 11)]
    my_asian_option.average_convention = average_convention
    my_market_data.underlying_spots = [100]
    my_market_data.risk_free_rate = 0.06
    my_market_data.dividend_rate = 0.03
    my_market_data.underlying_black_scholes_volatilities = [0.20]

    # Act
    result = price(my_asian_option, my_market_data, my_static_data, my_pricing_config)

    # Assert
    assert result['price'] == pytest.approx(expected_price, abs=1e-5)
