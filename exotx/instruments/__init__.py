"""Modules for working with exotic options.

Exotic options can refer to auto-callables, barrier options, etc."""

from exotx.instruments.autocallable import Autocallable
from exotx.instruments.barrier_option import BarrierOption
from exotx.instruments.instrument import price

__all__ = [
    'price',
    'Autocallable',
    'BarrierOption'
]
