from abc import ABC, abstractmethod


class Instrument(ABC):
    @abstractmethod
    def price(self, *args, **kwargs) -> float:
        pass


def price(instrument: Instrument, *args, **kwargs) -> float:
    return instrument.price(*args, **kwargs)
