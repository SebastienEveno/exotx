from datetime import datetime
from typing import Union

import QuantLib as ql
from marshmallow import Schema, fields, post_load

from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.helpers.dates import convert_maturity_to_ql_date
from exotx.instruments.instrument import Instrument
from exotx.instruments.option_type import convert_option_type_to_ql, OptionType, OptionTypeField
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.models.hestonmodel import HestonModel
from exotx.utils.pricing_configuration import PricingConfiguration


class VanillaOption(Instrument):
    """
    VanillaOption is a class representing a vanilla option financial instrument.

    A vanilla option is a financial derivative that gives the holder the right, but not the obligation, to buy or sell
    an underlying asset at a specific price on or before a specific date. The class inherits from the Instrument
    abstract base class and implements the price method to calculate the price of the vanilla option.

    The class supports multiple pricing models and numerical methods, as specified in the pricing configuration.

    Attributes:
    - strike (float): The option's strike price.
    - maturity (ql.Date): The option's maturity date in QuantLib format.
    - option_type (ql.Option.Type): The option type (call or put) in QuantLib format.

    Example usage:

    >>> vanilla_option = VanillaOption(strike=100.0, maturity='2023-05-10', option_type='call')
    >>> price = vanilla_option.price(market_data, static_data, pricing_config)
    """
    available_engines = {
        PricingModel.BLACK_SCHOLES: ql.AnalyticEuropeanEngine,
        PricingModel.HESTON: ql.AnalyticHestonEngine
    }

    def __init__(self, strike: float, maturity: Union[str, datetime], option_type: Union[str, OptionType]):
        assert strike >= 0, "Invalid strike: cannot be negative"
        self.strike = strike
        self.maturity = convert_maturity_to_ql_date(maturity)
        self.option_type = convert_option_type_to_ql(option_type)

    def price(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int = 1) -> dict:
        """
        Calculates the price and optionally the greeks (delta, gamma, and theta) for the vanilla option using the 
        provided market data, static data, and pricing configuration.

        :param market_data: Market data object containing relevant market information such as yield curve, dividend curve,
                            underlying spots, and volatilities.
        :type market_data: MarketData
        :param static_data: Static data object containing relevant static information such as calendar and day counter.
        :type static_data: StaticData
        :param pricing_config: Pricing configuration object containing pricing settings and whether to compute greeks.
        :type pricing_config: PricingConfiguration
        :param seed: Seed for the random number generator used in Monte Carlo pricing engine, defaults to 1.
        :type seed: int, optional
        :return: A dictionary containing the price and optionally the greeks (delta, gamma, and theta) of the option.
        :rtype: dict

        Example usage:

        >>> vanilla_option.price(market_data, static_data, pricing_config)
        {'price': 10.1234, 'delta': 0.5678, 'gamma': 0.0123, 'theta': -0.0987}
        """
        reference_date: ql.Date = market_data.get_ql_reference_date()
        ql.Settings.instance().evaluationDate = reference_date

        # create the product
        ql_payoff = ql.PlainVanillaPayoff(self.option_type, self.strike)
        ql_exercise = ql.EuropeanExercise(self.maturity)
        ql_option = ql.VanillaOption(ql_payoff, ql_exercise)

        # set the pricing engine
        ql_engine = self._get_ql_pricing_engine(
            market_data, static_data, pricing_config, seed)
        ql_option.setPricingEngine(ql_engine)

        # price
        price = ql_option.NPV()
        if pricing_config.compute_greeks and pricing_config.model != PricingModel.HESTON:
            delta = ql_option.delta()
            gamma = ql_option.gamma()
            theta = ql_option.theta()
            return {'price': price, 'delta': delta, 'gamma': gamma, 'theta': theta}
        else:
            return {'price': price}

    @staticmethod
    def _get_ql_pricing_engine(market_data, static_data, pricing_config: PricingConfiguration, seed: int):
        """
        Constructs the appropriate QuantLib pricing engine based on the provided pricing configuration.

        This function creates a Black-Scholes or Heston pricing engine depending on the specified pricing model
        and numerical method in the pricing configuration.

        :param market_data: Market data object containing relevant market information such as yield curve, dividend curve,
                            underlying spots, and volatilities.
        :type market_data: MarketData
        :param static_data: Static data object containing relevant static information such as calendar and day counter.
        :type static_data: StaticData
        :param pricing_config: Pricing configuration object containing pricing settings and whether to compute greeks.
        :type pricing_config: PricingConfiguration
        :param seed: Seed for the random number generator used in Monte Carlo pricing engine, defaults to 1.
        :type seed: int, optional
        :return: A QuantLib pricing engine for the specified pricing model and numerical method.
        :rtype: ql.PricingEngine

        Raises:
            ValueError: If an invalid combination of pricing model and numerical method is provided.
        """
        if pricing_config.model == PricingModel.BLACK_SCHOLES and \
                pricing_config.numerical_method == NumericalMethod.ANALYTIC:
            bs_model = BlackScholesModel(market_data, static_data)
            process = bs_model.setup()
            ql_engine = ql.AnalyticEuropeanEngine(process)
        elif pricing_config.model == PricingModel.HESTON and \
                pricing_config.numerical_method == NumericalMethod.ANALYTIC:
            heston_model = HestonModel(market_data, static_data)
            _, model = heston_model.calibrate(seed)
            ql_engine = ql.AnalyticHestonEngine(model)
        else:
            raise ValueError(f"Invalid pricing model {pricing_config.model} with numerical method "
                             f"{pricing_config.numerical_method}")

        return ql_engine

    # region serialization/deserialization
    def to_json(self):
        """
        Serializes the VanillaOption instance to a JSON representation using the VanillaOptionSchema.

        :return: A JSON representation of the VanillaOption instance.
        :rtype: dict
        """
        schema = VanillaOptionSchema()
        return schema.dump(self)

    @classmethod
    def from_json(cls, json_data):
        """
        Deserializes a JSON representation of a VanillaOption instance using the VanillaOptionSchema.

        :param json_data: A JSON representation of a VanillaOption instance.
        :type json_data: dict
        :return: A VanillaOption instance created from the JSON data.
        :rtype: VanillaOption
        """
        schema = VanillaOptionSchema()
        data = schema.load(json_data)
        return cls(**data)
    # endregion


# region Schema


class VanillaOptionSchema(Schema):
    """
    A Marshmallow schema for serializing and deserializing VanillaOption instances.

    The VanillaOptionSchema is used to define the structure of the JSON data for the VanillaOption class. It contains
    the fields required for a VanillaOption instance, such as strike, maturity, and option type.

    Attributes:
        strike (fields.Float): A Marshmallow field for the option's strike price.
        maturity (fields.Date): A Marshmallow field for the option's maturity date.
        option_type (OptionTypeField): A Marshmallow field for the option's type (call or put).
    """
    strike = fields.Float()
    maturity = fields.Date(format="%Y-%m-%d")
    option_type = OptionTypeField(allow_none=False)

    @post_load
    def make_vanilla_option(self, data, **kwargs) -> VanillaOption:
        """
        Constructs a VanillaOption instance from the deserialized data.

        This method is called by the Marshmallow schema after the input data has been deserialized.
        It uses the deserialized data to create a new VanillaOption instance and returns it.

        :param data: A dictionary containing the deserialized data for the vanilla option.
        :type data: dict
        :param kwargs: Additional keyword arguments.
        :return: A VanillaOption instance created from the deserialized data.
        :rtype: VanillaOption
        """
        return VanillaOption(**data)

# endregion
