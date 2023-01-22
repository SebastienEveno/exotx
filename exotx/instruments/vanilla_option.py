from typing import Union

import QuantLib as ql
from exotx.helpers.dates import convert_maturity_to_ql_date
from exotx.models.hestonmodel import HestonModel
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.enums.enums import PricingModelEnum, NumericalMethodEnum
from exotx.instruments.instrument import Instrument
from exotx.instruments.option_types import convert_option_type_to_ql, OptionTypeEnum
from exotx.utils.pricing_configuration import PricingConfiguration
from marshmallow import Schema, fields, post_load, ValidationError


class VanillaOption(Instrument):
    available_engines = {
        PricingModelEnum.BLACK_SCHOLES: ql.AnalyticEuropeanEngine,
        PricingModelEnum.HESTON: ql.AnalyticHestonEngine
    }

    def __init__(self, strike, maturity: Union[str, ql.Date], option_type: Union[str, OptionTypeEnum]):
        assert strike >= 0, "Invalid strike: cannot be negative"
        self.strike = strike
        self.maturity = convert_maturity_to_ql_date(maturity)
        self.option_type = convert_option_type_to_ql(option_type)

    def price(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int = 1) -> dict:
        reference_date: ql.Date = market_data.get_ql_reference_date()
        ql.Settings.instance().evaluationDate = reference_date

        # create the product
        ql_payoff = ql.PlainVanillaPayoff(self.option_type, self.strike)
        ql_exercise = ql.EuropeanExercise(self.maturity)
        ql_option = ql.VanillaOption(ql_payoff, ql_exercise)

        # set the pricing engine
        ql_engine = self._get_ql_pricing_engine(market_data, static_data, pricing_config, seed)
        ql_option.setPricingEngine(ql_engine)

        # price
        price = ql_option.NPV()
        if pricing_config.compute_greeks and pricing_config.model != PricingModelEnum.HESTON:
            delta = ql_option.delta()
            gamma = ql_option.gamma()
            theta = ql_option.theta()
            return {'price': price, 'delta': delta, 'gamma': gamma, 'theta': theta}
        else:
            return {'price': price}

    @staticmethod
    def _get_ql_pricing_engine(market_data, static_data, pricing_config: PricingConfiguration, seed: int):
        if pricing_config.model == PricingModelEnum.BLACK_SCHOLES and \
                pricing_config.numerical_method == NumericalMethodEnum.ANALYTIC:
            bs_model = BlackScholesModel(market_data, static_data)
            process = bs_model.setup()
            ql_engine = ql.AnalyticEuropeanEngine(process)
        elif pricing_config.model == PricingModelEnum.HESTON and \
                pricing_config.numerical_method == NumericalMethodEnum.ANALYTIC:
            heston_model = HestonModel(market_data, static_data)
            _, model = heston_model.calibrate(seed)
            ql_engine = ql.AnalyticHestonEngine(model)
        else:
            raise ValueError(f"Invalid pricing model {pricing_config.model} with numerical method {pricing_config.numerical_method}")

        return ql_engine

    def to_json(self):
        schema = VanillaOptionSchema()
        return schema.dump(self)

    @classmethod
    def from_json(cls, json_data):
        schema = VanillaOptionSchema()
        data = schema.load(json_data)
        return cls(**data)


# region Schema

class OptionTypeField(fields.Field):
    def _serialize(self, value: OptionTypeEnum, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> OptionTypeEnum:
        try:
            return OptionTypeEnum[value]
        except KeyError as error:
            raise ValidationError(f"Invalid option type \'{value}\'") from error


class VanillaOptionSchema(Schema):
    strike = fields.Float()
    maturity = fields.Date(format="%Y-%m-%d")
    option_type = OptionTypeField(allow_none=False)

    @post_load
    def make_vanilla_option(self, data, **kwargs) -> VanillaOption:
        return VanillaOption(**data)

# endregion
