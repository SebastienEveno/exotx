import pytest

from exotx import price
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.instruments.basket_option import BasketOption
from exotx.instruments.basket_type import BasketType
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
        'underlying_spots': [80, 90, 100],
        'risk_free_rate': 0.05,
        'dividend_rate': -0.03,
        'underlying_black_scholes_volatilities': [0.20, 0.25, 0.3],
        'correlation_matrix': [
            [1.0, 0.5, 0.6],
            [0.5, 1.0, 0.7],
            [0.6, 0.7, 1.0]
        ]
    }

    return MarketData.from_json(my_json)


@pytest.fixture
def my_basket_option() -> BasketOption:
    strike = 85
    maturity = '2016-02-04'  # reference_date + 90 days
    exercise = 'european'
    option_type = OptionType.PUT
    # option_type = 'call'
    basket_type = BasketType.MINBASKET

    return BasketOption(strike, maturity, option_type, basket_type)


@pytest.fixture
def my_pricing_config() -> PricingConfiguration:
    model = PricingModel.BLACK_SCHOLES
    numerical_method = NumericalMethod.ANALYTIC

    return PricingConfiguration(model, numerical_method)


@pytest.mark.parametrize(
    'expected_price',
    [
        5.7207
    ])
def test_price(my_basket_option: BasketOption,
               my_market_data: MarketData,
               my_static_data: StaticData,
               my_pricing_config: PricingConfiguration,
               expected_price: float) -> None:
    # Arrange
    seed = 42

    # Act
    result = price(my_basket_option, my_market_data, my_static_data, my_pricing_config, seed)

    # Assert
    assert result['price'] == pytest.approx(expected_price, abs=1e-4)
