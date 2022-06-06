import QuantLib as ql
import numpy as np
from typing import List, Tuple
from exotx.data.marketdata import MarketData


class BlackScholesModel:
    """Class for the Black-Scholes model."""

    def __init__(self,
                 reference_date: ql.Date,
                 calendar: ql.Calendar,
                 market_data: MarketData) -> None:
        self.reference_date = reference_date
        self.calendar = calendar
        self.market_data = market_data
        self._day_count = ql.Actual365Fixed()

    def setup_model(self) -> Tuple[ql.BlackScholesMertonProcess, ql.AnalyticEuropeanEngine]:
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.market_data.spot))
        flat_ts = self.market_data.get_yield_curve()
        dividend_yield = self.market_data.get_dividend_curve()
        flat_vol_ts = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(self.reference_date,
                                self.calendar,
                                self.market_data.black_scholes_volatility,
                                self._day_count)
        )
        process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
        engine = ql.AnalyticEuropeanEngine(process)

        return process, engine

    @staticmethod
    def generate_paths(dates,
                       day_counter: ql.DayCounter,
                       process: ql.BlackScholesMertonProcess,
                       number_of_paths: int = 100000,
                       seed: int = 1) -> np.ndarray:
        """Generate underlying and volatility paths."""
        dimension = process.factors()
        times = np.array([day_counter.yearFraction(dates[0], d) for d in dates])
        time_step = times.shape[0] - 1
        uniform_random_generator = ql.UniformRandomGenerator(seed=seed)
        sequence_generator = ql.UniformRandomSequenceGenerator(dimension * time_step, uniform_random_generator)
        gaussian_sequence_generator = ql.GaussianRandomSequenceGenerator(sequence_generator)
        paths_generator = ql.GaussianMultiPathGenerator(process, times, gaussian_sequence_generator)
        paths = np.zeros(shape=(number_of_paths, times.shape[0]))

        for i in range(number_of_paths):
            sample_path = paths_generator.next()
            values = sample_path.value()
            spot = values[0]
            # first argument refers to the underlying path, the second the volatility
            paths[i, :] = np.array(list(spot))

        return paths
