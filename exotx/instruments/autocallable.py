import QuantLib as ql
import numpy as np

from exotx.data.marketdata import MarketData
from exotx.data.staticdata import StaticData
from exotx.models.blackscholesmodel import BlackScholesModel
from exotx.models.hestonmodel import HestonModel


class Autocallable:
    """Class for modeling an autocallable and pricing it."""
    def __init__(self,
                 notional: int,
                 # observation_dates: List[datetime],
                 # redemption_levels: List[float],
                 strike: float,
                 autocall_barrier_level: float,
                 annual_coupon_value: float,
                 coupon_barrier_level: float,
                 # coupon_barrier_levels: List[float],
                 protection_barrier_level: float,
                 # annual_coupon_value: float,
                 has_memory: bool = False) -> None:
        assert notional > 0, "Notional equal to zero or is negative!"
        self.notional = notional

        assert strike > 0, "strike equal to zero or is negative!"
        self.strike = strike

        assert autocall_barrier_level > 0, "Autocall barrier level equal to zero or is negative!"
        self.autocall_barrier_level = autocall_barrier_level

        assert annual_coupon_value > 0, "Annual coupon value equal to zero or is negative!"
        self.annual_coupon_value = annual_coupon_value

        # assert len(observation_dates) > 0, "No observation dates!"
        # self.observation_dates = list(set(observation_dates))
        #
        # assert len(redemption_levels) > 0, "No redemption levels!"
        # self.redemption_levels = redemption_levels

        # assert len(coupon_barrier_levels) > 0, "No coupon barrier levels!"
        # self.coupon_barrier_levels = coupon_barrier_levels

        assert coupon_barrier_level > 0, "Coupon barrier level equal to zero or is negative!"
        self.coupon_barrier_level = coupon_barrier_level

        self.protection_barrier_level = protection_barrier_level
        # self.annual_coupon_value = annual_coupon_value
        self.has_memory = has_memory

    @staticmethod
    def _get_underlying_paths(dates: np.ndarray,
                              market_data: MarketData,
                              static_data: StaticData,
                              model: str,
                              seed: int = 1) -> np.ndarray:
        # set static data
        day_counter = static_data.get_ql_day_counter()

        if model.lower() == 'black-scholes':
            black_scholes_model = BlackScholesModel(market_data, static_data)
            process = black_scholes_model.setup()
            underlying_paths = black_scholes_model.generate_paths(dates, day_counter, process, seed=seed)[:, 1:]
        else:
            # defaults to Heston model
            # create and calibrate the heston model based on market data
            heston_model = HestonModel(market_data, static_data)
            process, model = heston_model.calibrate(seed=seed)
            # generate paths for a given set of dates, exclude the current spot rate
            underlying_paths = heston_model.generate_paths(dates, day_counter, process, seed=seed)[:, 1:]

        return underlying_paths

    def price(self, market_data: MarketData, static_data: StaticData, model: str, seed: int = 1):
        reference_date = market_data.reference_date
        ql.Settings.instance().evaluationDate = reference_date

        business_day_convention = static_data.get_default_ql_business_day_convention()
        calendar = static_data.get_ql_calendar()

        # coupon schedule
        start_date = reference_date
        first_coupon_date = calendar.advance(start_date, ql.Period(6, ql.Months))
        last_coupon_date = calendar.advance(start_date, ql.Period(3, ql.Years))
        coupon_dates = np.array(list(ql.Schedule(first_coupon_date, last_coupon_date, ql.Period(ql.Semiannual),
                                                 calendar, business_day_convention, business_day_convention,
                                                 ql.DateGeneration.Forward, False)))
        # create past fixings into dictionary
        past_fixings = {}

        # immediate exit trigger for matured transaction
        if reference_date >= coupon_dates[-1]:
            return 0.0

        # immediate exit trigger for any past autocall event
        if reference_date >= coupon_dates[0]:
            if max(past_fixings.values()) >= (self.autocall_barrier_level * self.strike):
                return 0.0

        # create date array for path generator
        # combine valuation date and all the remaining coupon dates
        dates = np.hstack((np.array([reference_date]), coupon_dates[coupon_dates > reference_date]))

        # get underlying paths
        paths = self._get_underlying_paths(dates, market_data, static_data, model, seed)

        # identify the past coupon dates
        past_coupon_dates = coupon_dates[coupon_dates <= reference_date]

        # conditionally, merge given past fixings from a given dictionary and generated paths
        if past_coupon_dates.shape[0] > 0:
            past_fixings_array = np.array([past_fixings[past_date] for past_date in past_coupon_dates])
            past_fixings_array = np.tile(past_fixings_array, (paths.shape[0], 1))
            paths = np.hstack((past_fixings_array, paths))

        # result accumulator
        global_pv = []
        expiration_date = coupon_dates[-1]
        has_memory = int(self.has_memory)

        # loop through all simulated paths
        for path in paths:
            payoff_present_value = 0.0
            unpaid_coupons = 0  # counter of unpaid coupons
            has_auto_called = False

            # loop through set of coupon dates and index ratios
            for previous_date, date, index in zip(dates, coupon_dates, path / self.strike):
                # if autocall event has been triggered, immediate exit from this path
                if has_auto_called:
                    break

                payoff = 0.0
                year_fraction = ql.Actual365Fixed().yearFraction(previous_date, date)
                # payoff calculation at expiration
                if date == expiration_date:
                    # index is greater or equal to coupon barrier level
                    # pay 100% redemption, plus coupon, plus conditionally all unpaid coupons
                    if index >= self.coupon_barrier_level:
                        payoff = self.notional * (1 + (self.annual_coupon_value * year_fraction * (1 + unpaid_coupons * has_memory)))
                    # index is greater or equal to protection barrier level and less than coupon barrier level
                    # pay 100% redemption, no coupon
                    if (index >= self.protection_barrier_level) & (index < self.coupon_barrier_level):
                        payoff = self.notional
                    # index is less than protection barrier
                    # pay redemption according to formula, no coupon
                    if index < self.protection_barrier_level:
                        payoff = self.notional * index
                # payoff calculation before expiration
                else:
                    # index is greater or equal to autocall barrier level
                    # autocall will happen before expiration
                    # pay 100% redemption, plus coupon, plus conditionally all unpaid coupons
                    if index >= self.autocall_barrier_level:
                        payoff = self.notional * (1 + (self.annual_coupon_value * year_fraction * (1 + unpaid_coupons * has_memory)))
                        has_auto_called = True
                    # index is greater or equal to coupon barrier level and less than autocall barrier level
                    # autocall will not happen
                    # pay coupon, plus conditionally all unpaid coupons
                    if (index >= self.coupon_barrier_level) & (index < self.autocall_barrier_level):
                        payoff = self.notional * (self.annual_coupon_value * year_fraction * (1 + unpaid_coupons * has_memory))
                        unpaid_coupons = 0
                    # index is less than coupon barrier level
                    # autocall will not happen
                    # no coupon payment, only accumulate unpaid coupons
                    if index < self.coupon_barrier_level:
                        payoff = 0.0
                        unpaid_coupons += 1

                # conditionally, calculate PV for period payoff, add PV to local accumulator
                if date > reference_date:
                    df = market_data.get_yield_curve().discount(date)
                    payoff_present_value += payoff * df

            # add path PV to global accumulator
            global_pv.append(payoff_present_value)

        return np.mean(np.array(global_pv))
