from datetime import datetime
from enum import Enum
from typing import Union, List

import QuantLib as ql
from marshmallow import Schema, fields, post_load, ValidationError

from exotx.enums.enums import PricingModel, NumericalMethod
from exotx.helpers.dates import convert_maturity_to_ql_date
from exotx.instruments.average_type import AverageTypeField, AverageType, convert_average_type_to_ql
from exotx.instruments.instrument import Instrument
from exotx.instruments.option_type import convert_option_type_to_ql, OptionType, OptionTypeField
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.utils.pricing_configuration import PricingConfiguration


class AverageCalculation(Enum):
    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'


class AverageCalculationField(fields.Field):
    def _serialize(self, value: AverageCalculation, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageCalculation:
        try:
            return AverageCalculation[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average calculation \"{value}\", expected one of {list(AverageCalculation.__members__.keys())}") from error


class AsianOption(Instrument):
    def __init__(self,
                 strike: float, maturity: Union[str, datetime], option_type: Union[str, OptionType],
                 average_type: Union[str, AverageType], average_calculation: Union[str, AverageCalculation],
                 arithmetic_running_accumulator: float = 0.0, geometric_running_accumulator: float = 1.0,
                 past_fixings: int = 0, future_fixing_dates: List[datetime] = None):
        assert strike >= 0, "Invalid strike: cannot be negative"
        self.strike = strike
        self.maturity = convert_maturity_to_ql_date(maturity)
        self.option_type = convert_option_type_to_ql(option_type)
        self.average_type = convert_average_type_to_ql(average_type)
        self.average_calculation: AverageCalculation = average_calculation
        self.arithmetic_running_accumulator = arithmetic_running_accumulator
        self.geometric_running_accumulator = geometric_running_accumulator
        self.past_fixings = past_fixings
        self.future_fixing_dates = None if not future_fixing_dates else [ql.Date().from_date(future_fixing_date)
                                                                         for future_fixing_date in future_fixing_dates]

    def price(self, market_data, static_data, pricing_config: PricingConfiguration, seed: int = 1) -> dict:
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
            ql_option = ql.ContinuousAveragingAsianOption(self.average_type, ql_payoff, ql_exercise)
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
                raise ValueError(f"Invalid average type \"{self.average_type}\"")
        else:
            raise ValueError(f"Invalid average calculation \"{self.average_calculation}\"")

        # set the pricing engine
        ql_engine = self._get_ql_pricing_engine(market_data, static_data, pricing_config, seed)
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
                    return ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
                elif pricing_config.numerical_method == NumericalMethod.MC:
                    # TODO: filter on pricing_config.pricing_model, here we assume black-scholes only
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    # TODO: get the traits parameter (lowdiscrepancy) from the pricing configuration
                    return ql.MCDiscreteGeometricAPEngine(process, "lowdiscrepancy")
                else:
                    raise ValueError(
                        f"No engine for asian option with numerical method {pricing_config.numerical_method}"
                        f"with average calculation {self.average_calculation} and average type {self.average_type}")
            elif self.average_type == ql.Average().Arithmetic:
                if pricing_config.numerical_method == NumericalMethod.MC:
                    bs_model = BlackScholesModel(market_data, static_data)
                    process = bs_model.setup()
                    return ql.MCDiscreteArithmeticAPEngine(process, "lowdiscrepancy")
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
            raise ValueError(f"Invalid average calculation \"{self.average_calculation}\"")

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


class AsianOptionSchema(Schema):
    strike = fields.Float()
    maturity = fields.Date(format="%Y-%m-%d")
    option_type = OptionTypeField(allow_none=False)
    average_type = AverageTypeField(allow_none=False)
    average_calculation = AverageCalculationField(allow_none=False)

    @post_load
    def make_asian_option(self, data, **kwargs) -> AsianOption:
        return AsianOption(**data)
