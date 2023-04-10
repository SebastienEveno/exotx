from enum import Enum
from typing import Union

import QuantLib as ql
from marshmallow import fields, ValidationError


class AverageType(Enum):
    ARITHMETIC = 'arithmetic'
    GEOMETRIC = 'geometric'


def convert_average_type_to_ql(average_type: Union[str, AverageType]):
    """
    Converts an AverageType enum value or a string representing an average type to the corresponding QuantLib average type.

    This function takes an input average_type, which can be either an AverageType enum value or a string, and returns the
    corresponding QuantLib average type (ql.Average().Arithmetic or ql.Average().Geometric). The function raises an error 
    if the input is invalid or not supported.

    :param average_type: The input average type, either as an AverageType enum value or a string.
    :type average_type: Union[str, AverageType]
    :return: The corresponding QuantLib average type (ql.Average().Arithmetic or ql.Average().Geometric).
    :rtype: ql.Average
    :raises ValueError: If the input average type is invalid or not supported.
    :raises TypeError: If the input type is not a valid AverageType enum value or a string.

    Example usage:

    >>> convert_average_type_to_ql(AverageType.ARITHMETIC)
    <AverageType.Arithmetic: 0>
    >>> convert_average_type_to_ql('geometric')
    <AverageType.Geometric: 1>
    """
    if isinstance(average_type, str):
        average_type = average_type.upper()
        if average_type not in AverageType.__members__:
            raise ValueError(
                f"Invalid average type \"{average_type}\", expected one of {list(AverageType.__members__.keys())}")
        return convert_average_type_to_ql(AverageType[average_type])
    elif isinstance(average_type, AverageType):
        if average_type == AverageType.ARITHMETIC:
            return ql.Average().Arithmetic
        elif average_type == AverageType.GEOMETRIC:
            return ql.Average().Geometric
        else:
            raise ValueError(f"Invalid average type \"{average_type}\"")
    else:
        raise TypeError(
            f"Invalid input type {type(average_type)} for average type")


class AverageTypeField(fields.Field):
    def _serialize(self, value: AverageType, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageType:
        try:
            return AverageType[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average type \"{value}\", expected one of {list(AverageType.__members__.keys())}") from error
