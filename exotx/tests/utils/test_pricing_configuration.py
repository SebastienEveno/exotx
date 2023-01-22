import pytest

from exotx.enums.enums import PricingModelEnum, NumericalMethodEnum
from exotx.utils.pricing_configuration import PricingConfiguration, PricingConfigurationSchema
from marshmallow import ValidationError


def test_to_json():
    pricing_config = PricingConfiguration(
        model=PricingModelEnum.BLACK_SCHOLES,
        numerical_method=NumericalMethodEnum.ANALYTIC,
        compute_greeks=True
    )
    json_data = pricing_config.to_json()

    assert json_data == {
        'model': 'BLACK_SCHOLES',
        'numerical_method': 'ANALYTIC',
        'compute_greeks': True
    }


def test_from_json():
    json_data = {
        'model': 'BLACK_SCHOLES',
        'numerical_method': 'ANALYTIC',
        'compute_greeks': True
    }

    pricing_config = PricingConfiguration.from_json(json_data)

    assert isinstance(pricing_config, PricingConfiguration)
    assert isinstance(pricing_config.model, PricingModelEnum)
    assert isinstance(pricing_config.numerical_method, NumericalMethodEnum)
    assert isinstance(pricing_config.compute_greeks, bool)

    assert pricing_config.model == PricingModelEnum.BLACK_SCHOLES
    assert pricing_config.numerical_method == NumericalMethodEnum.ANALYTIC
    assert pricing_config.compute_greeks == True


def test_from_json_invalid_model():
    json_data = {
        'model': 'INVALID_MODEL',
        'numerical_method': 'ANALYTIC',
        'compute_greeks': True
    }
    schema = PricingConfigurationSchema()
    with pytest.raises(ValidationError) as e:
        config = schema.load(json_data)
    assert 'model' in e.value.messages


def test_from_json_invalid_method():
    json_data = {
        'model': 'BLACK_SCHOLES',
        'numerical_method': 'INVALID_METHOD',
        'compute_greeks': True
    }
    schema = PricingConfigurationSchema()
    with pytest.raises(ValidationError) as e:
        config = schema.load(json_data)
    assert 'numerical_method' in e.value.messages