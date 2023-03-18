import pytest

from exotx import price
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.instruments.option_type import OptionType
from exotx.instruments.vanilla_option import VanillaOption
from exotx.utils.pricing_configuration import PricingConfiguration


# Arrange
@pytest.fixture
def my_vanilla_option() -> VanillaOption:
    strike = 90
    maturity = '2016-05-04'
    option_type = OptionType.CALL

    return VanillaOption(strike, maturity, option_type)


@pytest.fixture
def my_pricing_config() -> PricingConfiguration:
    model = PricingModel.BLACK_SCHOLES
    numerical_method = NumericalMethod.ANALYTIC
    compute_greeks = True

    return PricingConfiguration(model, numerical_method, compute_greeks=compute_greeks)


def test_price_compute_greeks_is_true(my_vanilla_option, my_market_data, my_static_data, my_pricing_config):
    # Act
    result = price(my_vanilla_option, my_market_data, my_static_data, my_pricing_config)

    # Assert
    assert 'price' in result
    assert 'delta' in result
    assert 'gamma' in result
    assert 'theta' in result


def test_price_compute_greeks_is_false(my_vanilla_option, my_market_data, my_static_data, my_pricing_config):
    # Arrange
    my_pricing_config.compute_greeks = False

    # Act
    result = price(my_vanilla_option, my_market_data, my_static_data, my_pricing_config)

    # Assert
    assert 'price' in result
    assert 'delta' not in result
    assert 'gamma' not in result
    assert 'theta' not in result


def test_price_invalid_model(my_vanilla_option, my_market_data, my_static_data, my_pricing_config):
    # Arrange
    my_pricing_config.model = 'invalid_model'

    # Act
    with pytest.raises(ValueError):
        price(my_vanilla_option, my_market_data, my_static_data, my_pricing_config)


@pytest.mark.parametrize(
    'strike, model, compute_greeks, expected_price, expected_delta, expected_gamma, expected_theta',
    [
        (90, PricingModel.BLACK_SCHOLES, True, 13.83328710, 0.77183751, 0.01609460, -7.01024983),
        (100, PricingModel.BLACK_SCHOLES, True, 7.84942762, 0.56837420, 0.02167605, -8.41931025),
        (110, PricingModel.BLACK_SCHOLES, True, 3.97951968, 0.36053753, 0.02089515, -7.65352494),
        (90, PricingModel.HESTON, False, 15.51921588, 0, 0, 0)
    ])
def test_price(my_vanilla_option: VanillaOption,
               my_market_data: MarketData,
               my_static_data: StaticData,
               my_pricing_config: PricingConfiguration,
               strike: float,
               model: str,
               compute_greeks: bool,
               expected_price: float,
               expected_delta: float,
               expected_gamma: float,
               expected_theta: float) -> None:
    # Arrange
    my_vanilla_option.strike = strike
    my_pricing_config.model = model
    my_pricing_config.compute_greeks = compute_greeks

    # Act
    result = price(my_vanilla_option, my_market_data, my_static_data, my_pricing_config, seed=125)

    # Assert
    assert result['price'] == pytest.approx(expected_price, abs=1e-4)
    if my_pricing_config.compute_greeks:
        assert result['delta'] == pytest.approx(expected_delta, abs=1e-8)
        assert result['gamma'] == pytest.approx(expected_gamma, abs=1e-8)
        assert result['theta'] == pytest.approx(expected_theta, abs=1e-8)
