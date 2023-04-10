from abc import ABC, abstractmethod
from typing import Union


class Instrument(ABC):
    @abstractmethod
    def price(self, *args, **kwargs) -> Union[float, dict]:
        """
        Abstract method to calculate the price of a financial instrument.

        This method should be implemented by subclasses to provide the pricing functionality 
        specific to the financial instrument they represent.

        :param args: Positional arguments to be passed to the price calculation.
        :param kwargs: Keyword arguments to be passed to the price calculation.
        :return: The price of the financial instrument, either as a single float or a dictionary 
                 containing additional information such as greeks.
        :rtype: Union[float, dict]
        """
        pass


def price(instrument: Instrument, *args, **kwargs) -> Union[float, dict]:
    """
    Calculates the price of the given financial instrument.

    This function serves as a wrapper around the price method of the Instrument class.
    It calls the price method on the given instrument instance and returns the result.

    :param instrument: An instance of a subclass of the Instrument class.
    :type instrument: Instrument
    :param args: Positional arguments to be passed to the price method of the instrument.
    :param kwargs: Keyword arguments to be passed to the price method of the instrument.
    :return: The price of the financial instrument, either as a single float or a dictionary 
             containing additional information such as greeks.
    :rtype: Union[float, dict]
    """
    return instrument.price(*args, **kwargs)
