from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class AverageCalculation(Enum):
    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'


def convert_average_calculation(average_calculation: Union[str, AverageCalculation]) -> AverageCalculation:
    """
    Converts an AverageCalculation enum value or a string representing an average calculation to the corresponding AverageCalculation enum value.

    This function takes an input average_calculation, which can be either an AverageCalculation enum value or a string, and returns the
    corresponding AverageCalculation enum value. The function raises an error if the input is invalid or not supported.

    :param average_calculation: The input average calculation, either as an AverageCalculation enum value or a string.
    :type average_calculation: Union[str, AverageCalculation]
    :return: The corresponding AverageCalculation enum value.
    :rtype: AverageCalculation
    :raises ValueError: If the input average calculation is invalid or not supported.
    :raises Exception: If the input type is not a valid AverageCalculation enum value or a string.

    Example usage:

    >>> convert_average_calculation(AverageCalculation.CONTINUOUS)
    <AverageCalculation.CONTINUOUS: 'continuous'>
    >>> convert_average_calculation('discrete')
    <AverageCalculation.DISCRETE: 'discrete'>
    """
    if isinstance(average_calculation, str):
        average_calculation = average_calculation.upper()
        if average_calculation not in AverageCalculation.__members__:
            raise ValueError(
                f"Invalid average calculation \"{average_calculation}\", expected one of {list(AverageCalculation.__members__.keys())}")
        return AverageCalculation[average_calculation]
    elif isinstance(average_calculation, AverageCalculation):
        return average_calculation
    else:
        raise Exception(
            f"Invalid average calculation type \"{type(average_calculation)}\"")


class AverageCalculationField(fields.Field):
    def _serialize(self, value: AverageCalculation, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageCalculation:
        try:
            return AverageCalculation[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average calculation \"{value}\", expected one of {list(AverageCalculation.__members__.keys())}") from error
