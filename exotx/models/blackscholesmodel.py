import QuantLib as ql
import numpy as np
from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData


class BlackScholesModel:
    """Class for the Black-Scholes model."""

    def __init__(self,
                 market_data: MarketData,
                 static_data: StaticData) -> None:
        self.reference_date = market_data.reference_date
        self.market_data = market_data
        # set static data
        self.calendar: ql.Calendar = static_data.get_ql_calendar()
        self._day_counter: ql.DayCounter = static_data.get_ql_day_counter()

    def setup(self) -> ql.BlackScholesMertonProcess:
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.market_data.spot))
        flat_ts = self.market_data.get_yield_curve()
        dividend_yield = self.market_data.get_dividend_curve()
        flat_vol_ts = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(self.reference_date,
                                self.calendar,
                                self.market_data.black_scholes_volatility,
                                self._day_counter)
        )
        process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

        return process

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
