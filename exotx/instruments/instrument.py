from abc import ABC, abstractmethod
from typing import Union


class Instrument(ABC):
    @abstractmethod
    def price(self, *args, **kwargs) -> Union[float, dict]:
        pass


def price(instrument: Instrument, *args, **kwargs) -> Union[float, dict]:
    return instrument.price(*args, **kwargs)
