import QuantLib as ql
import numpy as np
from scipy.optimize import differential_evolution
from typing import List, Tuple
from exotx.data.marketdata import MarketData


class HestonModel:
    """Class for the Heston model."""
    def __init__(self,
                 reference_date: ql.Date,
                 calendar: ql.Calendar,
                 market_data: MarketData) -> None:
        self.reference_date = reference_date
        self.calendar = calendar
        self.market_data = market_data
        self.initial_conditions = (0.02, 0.2, 0.5, 0.1, 0.01)
        self.bounds = [(0, 1.), (0.01, 15), (0.01, 1.), (-1, 1), (0, 1.)]

    def calibrate(self, seed: int = 1) -> Tuple[ql.HestonProcess, ql.HestonModel]:
        """Calibrate the Heston model."""
        process, model, engine = self._setup_model()
        helpers, grid_data = self._setup_helpers(engine)
        cost_function = self._cost_function_generator(model, helpers, norm=True)
        differential_evolution(cost_function, self.bounds, seed=seed, maxiter=100)
        print('Calibrated Heston parameters:', model.params())

        return process, model

    def _setup_model(self, initial_conditions: Tuple[float, ...] = None) -> Tuple[ql.HestonProcess,
                                                                                  ql.HestonModel,
                                                                                  ql.AnalyticHestonEngine]:
        if initial_conditions:
            theta, kappa, sigma, rho, v0 = initial_conditions
        else:
            theta, kappa, sigma, rho, v0 = self.initial_conditions

        process = ql.HestonProcess(self.market_data.get_yield_curve(),
                                   self.market_data.get_dividend_curve(),
                                   ql.QuoteHandle(ql.SimpleQuote(self.market_data.spot)),
                                   v0, kappa, theta, sigma, rho)
        model = ql.HestonModel(process)
        engine = ql.AnalyticHestonEngine(model)

        return process, model, engine

    def _setup_helpers(self, engine: ql.AnalyticHestonEngine) -> Tuple[List[ql.HestonModelHelper],
                                                                       List[Tuple[ql.Date, float]]]:
        helpers = []
        grid_data = []
        for i, date in enumerate([ql.Date().from_date(date) for date in self.market_data.expiration_dates]):
            for j, strike in enumerate(self.market_data.strikes):
                t = (date - self.reference_date)
                p = ql.Period(t, ql.Days)
                vols = self.market_data.data[i][j]
                helper = ql.HestonModelHelper(
                    p, self.calendar, self.market_data.spot, strike,
                    ql.QuoteHandle(ql.SimpleQuote(vols)),
                    self.market_data.get_yield_curve(), self.market_data.get_dividend_curve())
                helper.setPricingEngine(engine)
                helpers.append(helper)
                grid_data.append((date, strike))

        return helpers, grid_data

    @staticmethod
    def _cost_function_generator(model: ql.HestonModel, helpers: List[ql.HestonModelHelper], norm=False):
        def cost_function(params):
            params_ = ql.Array(list(params))
            model.setParams(params_)
            error = [h.calibrationError() for h in helpers]
            if norm:
                return np.sqrt(np.sum(np.abs(error)))
            else:
                return error

        return cost_function

    @staticmethod
    def generate_paths(dates,
                       day_counter: ql.DayCounter,
                       process: ql.HestonProcess,
                       number_of_paths: int = 10000,
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

        # return array dimensions: [number of paths, number of items in t array]
        return paths
