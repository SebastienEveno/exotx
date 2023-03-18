from enum import Enum


class PricingModel(Enum):
    BLACK_SCHOLES = "BlackScholes"
    HESTON = "Heston"

    @staticmethod
    def values():
        return [e.value for e in PricingModel]


class NumericalMethod(Enum):
    PDE = "PDE"
    MC = "MC"
    ANALYTIC = "ANALYTIC"

    @staticmethod
    def values():
        return [e.value for e in NumericalMethod]


class RandomNumberGenerator(Enum):
    PSEUDORANDOM = "pseudorandom"
    LOWDISCREPANCY = "lowdiscrepancy"

    @staticmethod
    def values():
        return [e.value for e in RandomNumberGenerator]
