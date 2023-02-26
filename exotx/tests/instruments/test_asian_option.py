from datetime import timedelta
import pytest
import QuantLib as ql
from exotx import price
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.instruments.asian_option import AsianOption, AverageCalculation
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
        'spot': 80,
        'risk_free_rate': 0.05,
        'dividend_rate': -0.03,
        'black_scholes_volatility': 0.20
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

    return AsianOption(strike, maturity, option_type, average_type, average_calculation)


@pytest.fixture
def my_pricing_config() -> PricingConfiguration:
    model = PricingModel.BLACK_SCHOLES
    numerical_method = NumericalMethod.ANALYTIC
    compute_greeks = True

    return PricingConfiguration(model, numerical_method, compute_greeks)


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
