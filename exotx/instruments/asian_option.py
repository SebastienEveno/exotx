from datetime import datetime
from typing import Union, List

import QuantLib as ql
from marshmallow import Schema, fields, post_load

from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.helpers.dates import convert_maturity_to_ql_date
from exotx.instruments.average_calculation import AverageCalculation, convert_average_calculation, \
    AverageCalculationField
from exotx.instruments.average_convention import AverageConvention, convert_average_convention, AverageConventionField
from exotx.instruments.average_type import AverageTypeField, AverageType, convert_average_type_to_ql
from exotx.instruments.instrument import Instrument
from exotx.instruments.option_type import convert_option_type_to_ql, OptionType, OptionTypeField
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.utils.pricing_configuration import PricingConfiguration


class AsianOption(Instrument):
    """
    A class representing an Asian option, which is an option type that derives its value from the average price of
    the underlying asset over a specified period.

    The AsianOption class extends the Instrument class and provides functionality for constructing and pricing
    Asian options using the QuantLib library.

    Attributes:
        strike (float): The strike price of the option.
        maturity (Union[str, datetime]): The maturity date of the option as a string or datetime object.
        option_type (Union[str, OptionType]): The type of the option (call or put) as a string or OptionType object.
        average_type (Union[str, AverageType]): The averaging type of the option as a string or AverageType object.
        average_calculation (Union[str, AverageCalculation]): The average calculation method for the option as a string or AverageCalculation object.
        average_convention (Union[str, AverageConvention]): The averaging convention of the option as a string or AverageConvention object.
        arithmetic_running_accumulator (float, optional): The arithmetic running accumulator for the option. Defaults to 0.0.
        geometric_running_accumulator (float, optional): The geometric running accumulator for the option. Defaults to 1.0.
        past_fixings (int, optional): The number of past fixings for the option. Defaults to 0.
        future_fixing_dates (List[datetime], optional): A list of future fixing dates for the option. Defaults to None.
    """

    def __init__(self,
                 strike: float, maturity: Union[str, datetime], option_type: Union[str, OptionType],
                 average_type: Union[str, AverageType], average_calculation: Union[str, AverageCalculation],
                 average_convention: Union[str, AverageConvention], arithmetic_running_accumulator: float = 0.0,
                 geometric_running_accumulator: float = 1.0, past_fixings: int = 0,
                 future_fixing_dates: List[datetime] = None):
        assert strike >= 0, "Invalid strike: cannot be negative"
        self.strike = strike
        self.maturity = convert_maturity_to_ql_date(maturity)
        self.option_type = convert_option_type_to_ql(option_type)
        self.average_type = convert_average_type_to_ql(average_type)
        self.average_calculation: AverageCalculation = convert_average_calculation(
            average_calculation)
        self.average_convention: AverageConvention = convert_average_convention(
            average_convention)
        self.arithmetic_running_accumulator = arithmetic_running_accumulator
        self.geometric_running_accumulator = geometric_running_accumulator
        self.past_fixings = past_fixings
        self.future_fixing_dates = None if not future_fixing_dates else [ql.Date().from_date(future_fixing_date)
                                                                         for future_fixing_date in future_fixing_dates]

    def price(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int = 1) -> dict:
        """
        Prices the Asian option using the given market data, static data, and pricing configuration.

        :param market_data: An object containing the market data needed to price the option.
        :type market_data: MarketData
        :param static_data: An object containing the static data needed to price the option.
        :type static_data: StaticData
        :param pricing_config: A configuration object for the pricing process.
        :type pricing_config: PricingConfiguration
        :param seed: An optional integer seed for random number generation. Defaults to 1.
        :type seed: int
        :return: A dictionary containing the option price and, if applicable, Greeks.
        :rtype: dict
        """
        reference_date: ql.Date = market_data.get_ql_reference_date()
        ql.Settings.instance().evaluationDate = reference_date

        # check future fixing dates
        if self.future_fixing_dates:
            for future_fixing_date in self.future_fixing_dates:
                assert future_fixing_date >= reference_date, f"Invalid future fixing date {future_fixing_date}"

        # create the product
        ql_payoff = ql.PlainVanillaPayoff(self.option_type, self.strike)
        ql_exercise = ql.EuropeanExercise(self.maturity)
        if self.average_calculation == AverageCalculation.CONTINUOUS:
            ql_option = ql.ContinuousAveragingAsianOption(
                self.average_type, ql_payoff, ql_exercise)
        elif self.average_calculation == AverageCalculation.DISCRETE:
            if self.average_type == ql.Average().Arithmetic:
                ql_option = ql.DiscreteAveragingAsianOption(self.average_type,
                                                            self.arithmetic_running_accumulator,
                                                            self.past_fixings, self.future_fixing_dates, ql_payoff,
                                                            ql_exercise)
            elif self.average_type == ql.Average().Geometric:
                ql_option = ql.DiscreteAveragingAsianOption(self.average_type, self.geometric_running_accumulator,
                                                            self.past_fixings, self.future_fixing_dates, ql_payoff,
                                                            ql_exercise)
            else:
                raise ValueError(
                    f"Invalid average type \"{self.average_type}\"")
        else:
            raise ValueError(
                f"Invalid average calculation \"{self.average_calculation}\"")

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

    def _get_ql_pricing_engine(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int):
        if self.average_calculation == AverageCalculation.DISCRETE:
            if self.average_type == ql.Average().Geometric:
                if pricing_config.numerical_method == NumericalMethod.ANALYTIC:
                    # TODO: filter on pricing_config.pricing_model, here we assume black-scholes only
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    if self.average_convention == AverageConvention.PRICE:
                        return ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
                    elif self.average_convention == AverageConvention.STRIKE:
                        return ql.AnalyticDiscreteGeometricAverageStrikeAsianEngine(process)
                    else:
                        raise ValueError(
                            f"Invalid average convention \"{self.average_convention}\"")
                elif pricing_config.numerical_method == NumericalMethod.MC:
                    # TODO: filter on pricing_config.pricing_model, here we assume black-scholes only
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    random_number_generator = str(
                        pricing_config.random_number_generator)
                    if self.average_convention == AverageConvention.PRICE:
                        return ql.MCDiscreteGeometricAPEngine(process, random_number_generator)
                    elif self.average_convention == AverageConvention.STRIKE:
                        return ValueError(
                            f"No corresponding engine for asian option for numerical method {pricing_config.numerical_method}, "
                            f"average type {self.average_type}, average calculation {self.average_calculation}, and average convention {self.average_convention}")
                    else:
                        raise ValueError(
                            f"Invalid average convention \"{self.average_convention}\"")
                else:
                    raise ValueError(
                        f"No engine for asian option with numerical method {pricing_config.numerical_method}"
                        f"with average calculation {self.average_calculation} and average type {self.average_type}")
            elif self.average_type == ql.Average().Arithmetic:
                if pricing_config.numerical_method == NumericalMethod.MC:
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    random_number_generator = str(
                        pricing_config.random_number_generator)
                    if self.average_convention == AverageConvention.PRICE:
                        return ql.MCDiscreteArithmeticAPEngine(process, random_number_generator)
                    elif self.average_convention == AverageConvention.STRIKE:
                        return ql.MCDiscreteArithmeticASEngine(process, random_number_generator)
                    else:
                        raise ValueError(
                            f"Invalid average convention \"{self.average_convention}\"")
            else:
                raise ValueError(f"Invalid average type {self.average_type}")
        elif self.average_calculation == AverageCalculation.CONTINUOUS:
            if self.average_type == ql.Average().Geometric:
                if pricing_config.numerical_method == NumericalMethod.ANALYTIC:
                    # TODO: filter on pricing_config.pricing_model, here we assume black-scholes only
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    return ql.AnalyticContinuousGeometricAveragePriceAsianEngine(process)
                else:
                    raise ValueError(
                        f"No engine for asian option with numerical method {pricing_config.numerical_method}"
                        f"with average calculation {self.average_calculation} and average type {self.average_type}")
            else:
                raise ValueError("No engine for asian option")
        else:
            raise ValueError(
                f"Invalid average calculation \"{self.average_calculation}\"")

    # region serialization/deserialization
    def to_json(self):
        schema = AsianOptionSchema()
        return schema.dump(self)

    @classmethod
    def from_json(cls, json_data):
        schema = AsianOptionSchema()
        data = schema.load(json_data)
        return cls(**data)
    # endregion


# region Schema
class AsianOptionSchema(Schema):
    """
    AsianOptionSchema is a Marshmallow schema class for deserializing and validating JSON data into an AsianOption object.

    This schema defines the required fields for an AsianOption object and validates their types and values. It also provides
    a post_load method to create an AsianOption object after deserialization and validation.

    Fields:
    - strike (float): The option's strike price.
    - maturity (date): The option's maturity date in the format "YYYY-MM-DD".
    - option_type (OptionType): The option type, either "call" or "put".
    - average_type (AverageType): The averaging type, either "arithmetic" or "geometric".
    - average_calculation (AverageCalculation): The averaging calculation, either "continuous" or "discrete".
    - average_convention (AverageConvention): The average convention, either "price" or "strike".

    Example usage:

    >>> asian_option_data = {
    ...     "strike": 100.0,
    ...     "maturity": "2023-05-10",
    ...     "option_type": "call",
    ...     "average_type": "arithmetic",
    ...     "average_calculation": "continuous",
    ...     "average_convention": "price"
    ... }
    >>> schema = AsianOptionSchema()
    >>> result = schema.load(asian_option_data)
    >>> asian_option = result.data
    """
    strike = fields.Float()
    maturity = fields.Date(format="%Y-%m-%d")
    option_type = OptionTypeField()
    average_type = AverageTypeField()
    average_calculation = AverageCalculationField()
    average_convention = AverageConventionField()

    @post_load
    def make_asian_option(self, data, **kwargs) -> AsianOption:
        """
        Creates an AsianOption object after deserialization and validation of JSON data.

        This method is called after the JSON data has been deserialized and validated against the schema. It constructs
        an AsianOption object using the deserialized data.

        :param data: The deserialized and validated JSON data.
        :type data: dict
        :return: The created AsianOption object.
        :rtype: AsianOption
        """
        return AsianOption(**data)
# endregion
