from datetime import datetime
from enum import Enum

import QuantLib as ql

from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.instruments.instrument import Instrument
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.models.hestonmodel import HestonModel


class OptionType(Enum):
    CALL = 'call'
    PUT = 'put'


class BarrierType(Enum):
    DOWNANDIN = 'downandin'
    DOWNANDOUT = 'downandout'
    UPANDIN = 'upandin'
    UPANDOUT = 'upandout'


class ExerciseType(Enum):
    EUROPEAN = 'european'
    AMERICAN = 'american'


class BarrierOptionEngine(Enum):
    ANALYTICBARRIERENGINE = 'analytic'
    FDBLACKSCHOLESBARRIERENGINE = 'fd-bs-barrier'
    FDBLACKSCHOLESREBATEENGINE = 'fd-bs-rebate'
    FDHESTONBARRIERENGINE = 'fd-heston-barrier'


class BarrierOption(Instrument):
    """
    BarrierOption is a class representing a barrier option financial instrument.

    The BarrierOption class provides methods for pricing and analyzing barrier options using various models
    and pricing engines from the QuantLib library.

    Attributes:
        barrier_type (BarrierType): The barrier type (Up-and-In, Up-and-Out, Down-and-In, or Down-and-Out).
        barrier (float): The barrier level.
        strike (float): The strike price of the option.
        maturity (ql.Date): The maturity date of the option.
        exercise (ExerciseType): The exercise style (European or American).
        option_type (OptionType): The option type (Call or Put).
        rebate (float): The rebate amount.
        reference_date (ql.Date): The reference date used for pricing the option.
        model (str): The pricing model used for the option.
    """

    def __init__(self,
                 barrier_type: str,
                 barrier: float,
                 strike: float,
                 maturity: str,
                 exercise: str = 'european',
                 option_type: str = 'call',
                 rebate: float = 0):
        self.barrier_type = BarrierType[barrier_type.upper()]
        self.barrier = barrier
        self.strike = strike
        self.maturity = ql.Date().from_date(datetime.strptime(maturity, "%Y-%m-%d"))
        self.exercise = ExerciseType[exercise.upper()]
        self.option_type = OptionType[option_type.upper()]
        self.rebate = rebate
        self.reference_date = ql.Date().todaysDate()
        self.model = None

    def price(self, market_data: MarketData, static_data: StaticData, model: str):
        """
        Calculates the price of the barrier option using the given market data, static data, and model.

        :param market_data: The market data used for pricing the option.
        :type market_data: MarketData
        :param static_data: The static data used for pricing the option.
        :type static_data: StaticData
        :param model: The pricing model used for the option.
        :type model: str
        :return: The net present value (NPV) of the option.
        :rtype: float
        """
        self.reference_date: ql.Date = market_data.get_ql_reference_date()
        ql.Settings.instance().evaluationDate = self.reference_date

        # create product
        ql_barrier_type = self._get_ql_barrier_type()
        ql_payoff = self._get_ql_payoff()
        ql_exercise = self._get_ql_exercise()
        ql_option = ql.BarrierOption(
            ql_barrier_type, self.barrier, self.rebate, ql_payoff, ql_exercise)

        # set pricing engine
        ql_pricing_engine = self._get_ql_pricing_engine(
            market_data, static_data, model)
        ql_option.setPricingEngine(ql_pricing_engine)

        return ql_option.NPV()

    def _get_ql_barrier_type(self) -> ql.Barrier:
        if self.barrier_type == BarrierType.UPANDIN:
            return ql.Barrier.UpIn
        elif self.barrier_type == BarrierType.UPANDOUT:
            return ql.Barrier.UpOut
        elif self.barrier_type == BarrierType.DOWNANDIN:
            return ql.Barrier.DownIn
        else:
            return ql.Barrier.DownOut

    def _get_ql_pricing_engine(self, market_data: MarketData, static_data: StaticData, model: str):
        model = model.lower()
        assert model in [engine.value for engine in BarrierOptionEngine]
        engine = BarrierOptionEngine(model)

        if engine == BarrierOptionEngine.ANALYTICBARRIERENGINE:
            bs_model = BlackScholesModel(market_data, static_data)
            process = bs_model.setup()
            return ql.AnalyticBarrierEngine(process)
        elif engine == BarrierOptionEngine.FDBLACKSCHOLESBARRIERENGINE:
            bs_model = BlackScholesModel(market_data, static_data)
            process = bs_model.setup()
            return ql.FdBlackScholesBarrierEngine(process)
        elif engine == BarrierOptionEngine.FDBLACKSCHOLESREBATEENGINE:
            bs_model = BlackScholesModel(market_data, static_data)
            process = bs_model.setup()
            return ql.FdBlackScholesRebateEngine(process)
        elif engine == BarrierOptionEngine.FDHESTONBARRIERENGINE:
            heston_model = HestonModel(market_data, static_data)
            _, model = heston_model.calibrate()
            return ql.FdHestonBarrierEngine(model)
        else:
            raise NotImplementedError

    def _get_ql_option_type(self):
        if self.option_type == OptionType.CALL:
            return ql.Option.Call
        else:
            return ql.Option.Put

    def _get_ql_payoff(self) -> ql.Payoff:
        ql_option_type = self._get_ql_option_type()
        # TODO: Consider different payoffs?
        return ql.PlainVanillaPayoff(ql_option_type, self.strike)

    def _get_ql_exercise(self) -> ql.Exercise:
        if self.exercise == ExerciseType.EUROPEAN:
            return ql.EuropeanExercise(self.maturity)
        else:
            return ql.AmericanExercise(self.reference_date, self.maturity)
