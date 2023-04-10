from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class AverageConvention(Enum):
    PRICE = 'price'
    STRIKE = 'strike'


def convert_average_convention(average_convention: Union[str, AverageConvention]) -> AverageConvention:
    """
    Converts an AverageConvention enum value or a string representing an average convention to the corresponding AverageConvention enum value.

    This function takes an input average_convention, which can be either an AverageConvention enum value or a string, and returns the
    corresponding AverageConvention enum value. The function raises an error if the input is invalid or not supported.

    :param average_convention: The input average convention, either as an AverageConvention enum value or a string.
    :type average_convention: Union[str, AverageConvention]
    :return: The corresponding AverageConvention enum value.
    :rtype: AverageConvention
    :raises ValueError: If the input average convention is invalid or not supported.
    :raises Exception: If the input type is not a valid AverageConvention enum value or a string.

    Example usage:

    >>> convert_average_convention(AverageConvention.PRICE)
    <AverageConvention.PRICE: 'price'>
    >>> convert_average_convention('strike')
    <AverageConvention.STRIKE: 'strike'>
    """
    if isinstance(average_convention, str):
        average_convention = average_convention.upper()
        if average_convention not in AverageConvention.__members__:
            raise ValueError(
                f"Invalid average convention \"{average_convention}\", expected one of {list(AverageConvention.__members__.keys())}")
        return AverageConvention[average_convention]
    elif isinstance(average_convention, AverageConvention):
        return average_convention
    else:
        raise Exception(
            f"Invalid average convention type \"{type(average_convention)}\"")


class AverageConventionField(fields.Field):
    def _serialize(self, value: AverageConvention, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageConvention:
        try:
            return AverageConvention[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average convention \"{value}\", expected one of {list(AverageConvention.__members__.keys())}") from error
