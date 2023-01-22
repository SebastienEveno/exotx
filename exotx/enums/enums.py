from enum import Enum


class PricingModelEnum(Enum):
    BLACK_SCHOLES = "BlackScholes"
    HESTON = "Heston"

    @staticmethod
    def values():
        return [e.value for e in PricingModelEnum]


class NumericalMethodEnum(Enum):
    PDE = "PDE"
    MC = "MC"
    ANALYTIC = "ANALYTIC"

    @staticmethod
    def values():
        return [e.value for e in NumericalMethodEnum]
