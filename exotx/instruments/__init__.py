"""Modules for working with exotic options.

Exotic options can refer to auto-callables, barrier options, etc."""

from exotx.instruments.autocallable import Autocallable
from exotx.instruments.barrier_option import BarrierOption
from exotx.instruments.instrument import price
from exotx.instruments.option_type import OptionType

__all__ = [
    'price',
    'Autocallable',
    'BarrierOption',
    'OptionType'
]
