from datetime import datetime
from typing import Union

import QuantLib as ql
from marshmallow import Schema, fields, post_load

from exotx.enums.enums import RandomNumberGenerator
from exotx.helpers.dates import convert_maturity_to_ql_date
from exotx.instruments.basket_type import BasketType, convert_basket_type, BasketTypeField
from exotx.instruments.instrument import Instrument
from exotx.instruments.option_type import convert_option_type_to_ql, OptionType, OptionTypeField
from exotx.utils.pricing_configuration import PricingConfiguration


class BasketOption(Instrument):
    """
    BasketOption is a class representing a basket option financial instrument.

    A basket option is a financial derivative that derives its value from the weighted sum of several underlying assets.
    The class inherits from the Instrument abstract base class and implements the price method to calculate the price of
    the basket option.

    The class also provides methods for converting basket type to the corresponding QuantLib payoff and creating a
    QuantLib pricing engine for the basket option.

    Attributes:
    - strike (float): The option's strike price.
    - maturity (ql.Date): The option's maturity date in QuantLib format.
    - option_type (ql.Option.Type): The option type (call or put) in QuantLib format.
    - basket_type (BasketType): The basket type (minbasket, maxbasket, spreadbasket, or averagebasket).

    Example usage:

    >>> basket_option = BasketOption(strike=100.0, maturity='2023-05-10', option_type='call', basket_type='minbasket')
    >>> price = basket_option.price(market_data, static_data, pricing_config)
    """

    def __init__(self,
                 strike: float,
                 maturity: Union[str, datetime],
                 option_type: Union[str, OptionType],
                 basket_type: Union[str, BasketType]):
        assert strike >= 0, "Invalid strike: cannot be negative"
        self.strike = strike
        self.maturity = convert_maturity_to_ql_date(maturity)
        self.option_type = convert_option_type_to_ql(option_type)
        self.basket_type = convert_basket_type(basket_type)

    def price(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int = 1) -> dict:
        """
        Calculates the price and optionally the greeks (delta, gamma, and theta) for the basket option using the 
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

        >>> basket_option.price(market_data, static_data, pricing_config)
        {'price': 10.1234, 'delta': 0.5678, 'gamma': 0.0123, 'theta': -0.0987}
        """
        # set the reference date
        reference_date: ql.Date = market_data.get_ql_reference_date()
        ql.Settings.instance().evaluationDate = reference_date

        # create the product
        ql_payoff = ql.PlainVanillaPayoff(self.option_type, self.strike)
        ql_exercise = ql.EuropeanExercise(self.maturity)

        ql_basket_payoff = self._basket_type_to_payoff(ql_payoff)
        ql_option = ql.BasketOption(ql_basket_payoff, ql_exercise)

        # set the pricing engine
        ql_engine = self._get_ql_pricing_engine(
            market_data, static_data, pricing_config, seed)
        ql_option.setPricingEngine(ql_engine)

        # price
        price = ql_option.NPV()
        if pricing_config.compute_greeks:
            delta = ql_option.delta()
            gamma = ql_option.gamma()
            theta = ql_option.theta()
            return {'price': price, 'delta': delta, 'gamma': gamma, 'theta': theta}
        else:
            return {'price': price}

    def _basket_type_to_payoff(self, payoff: ql.PlainVanillaPayoff):
        """
        Converts a plain vanilla payoff to a basket payoff based on the basket type.

        Args:
            payoff (ql.PlainVanillaPayoff): A plain vanilla payoff object from QuantLib.

        Returns:
            ql.BasketPayoff: A QuantLib BasketPayoff object corresponding to the specified basket type.

        Raises:
            Exception: If the basket type is not one of the supported types (MINBASKET, MAXBASKET, SPREADBASKET, AVERAGEBASKET).
        """
        if self.basket_type == BasketType.MINBASKET:
            return ql.MinBasketPayoff(payoff)
        elif self.basket_type == BasketType.MAXBASKET:
            return ql.MaxBasketPayoff(payoff)
        elif self.basket_type == BasketType.SPREADBASKET:
            return ql.SpreadBasketPayoff(payoff)
        elif self.basket_type == BasketType.AVERAGEBASKET:
            return ql.AverageBasketPayoff(payoff)
        else:
            raise Exception("Invalid basket type")

    @staticmethod
    def _get_ql_pricing_engine(market_data, static_data, pricing_config: PricingConfiguration, seed: int):
        """
        Constructs a QuantLib MCEuropeanBasketEngine for pricing basket options using Monte Carlo simulations.

        This function creates a list of Black-Scholes-Merton processes for each underlying asset, using the spot prices
        and volatilities provided by the MarketData instance. The processes are then combined into a StochasticProcessArray,
        taking into account the correlation matrix from the MarketData instance.

        Finally, a MCEuropeanBasketEngine is constructed using the StochasticProcessArray, along with the specified
        random number generator, time steps per year, required samples, and random seed.

        Args:
            market_data (MarketData): A MarketData instance containing the required market data, including underlying
                                      spot prices, volatilities, and the correlation matrix.
            static_data (StaticData): A StaticData instance containing static information such as calendar and day counter.
            seed (int): A random seed for the Monte Carlo simulations.

        Returns:
            ql.MCEuropeanBasketEngine: A QuantLib MCEuropeanBasketEngine for pricing basket options.

        Note:
            The current implementation only supports MCEuropeanBasketEngine. Additional pricing engines can be added
            based on the basket type and/or pricing configuration.
        """

        # set the reference date
        reference_date = market_data.get_ql_reference_date()

        # set static data
        calendar = static_data.get_ql_calendar()
        day_counter = static_data.get_ql_day_counter()

        processes = [ql.BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(x)),
                                                  market_data.get_dividend_curve(
                                                      day_counter),
                                                  market_data.get_yield_curve(
                                                      day_counter),
                                                  ql.BlackVolTermStructureHandle(
                                                      ql.BlackConstantVol(reference_date, calendar, y, day_counter)))
                     for x, y in zip(market_data.underlying_spots, market_data.underlying_black_scholes_volatilities)]
        multi_processes = ql.StochasticProcessArray(
            processes, market_data.get_correlation_matrix())

        # TODO: Consider different pricing engines based on self.basket_type and/or pricing_config
        return ql.MCEuropeanBasketEngine(multi_processes, RandomNumberGenerator.PSEUDORANDOM.value, timeStepsPerYear=1,
                                         requiredSamples=100000, seed=seed)


# region Schema
class BasketOptionSchema(Schema):
    """
    BasketOptionSchema is a Marshmallow schema class for deserializing and validating JSON data into a BasketOption object.

    This schema defines the required fields for a BasketOption object and validates their types and values. It also provides
    a post_load method to create a BasketOption object after deserialization and validation.

    Fields:
    - strike (float): The option's strike price.
    - maturity (date): The option's maturity date in the format "YYYY-MM-DD".
    - option_type (OptionType): The option type, either "call" or "put".
    - basket_type (BasketType): The basket type, one of "minbasket", "maxbasket", "spreadbasket", or "averagebasket".

    Example usage:

    >>> basket_option_data = {
    ...     "strike": 100.0,
    ...     "maturity": "2023-05-10",
    ...     "option_type": "call",
    ...     "basket_type": "minbasket"
    ... }
    >>> schema = BasketOptionSchema()
    >>> result = schema.load(basket_option_data)
    >>> basket_option = result.data
    """
    strike = fields.Float()
    maturity = fields.Date(format="%Y-%m-%d")
    option_type = OptionTypeField()
    basket_type = BasketTypeField()

    @post_load
    def make_basket_option(self, data, **kwargs) -> BasketOption:
        """
        Constructs a BasketOption instance from the deserialized data.

        This method is called by the Marshmallow schema after the input data has been deserialized.
        It uses the deserialized data to create a new BasketOption instance and returns it.

        :param data: A dictionary containing the deserialized data for the basket option.
        :type data: dict
        :param kwargs: Additional keyword arguments.
        :return: A BasketOption instance created from the deserialized data.
        :rtype: BasketOption
        """
        return BasketOption(**data)
# endregion
