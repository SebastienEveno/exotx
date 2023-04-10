from enum import Enum
from typing import Union

import QuantLib as ql
from marshmallow import fields, ValidationError


class OptionType(Enum):
    CALL = 'call'
    PUT = 'put'

    @staticmethod
    def values():
        return [e.value for e in OptionType]


def convert_option_type_to_ql(option_type: Union[str, OptionType]) -> ql.Option:
    """
    Converts an OptionType enum value or a string representing an option type to the corresponding QuantLib option type.

    This function takes an input option_type, which can be either an OptionType enum value or a string, and returns the
    corresponding QuantLib option type (ql.Option.Call or ql.Option.Put). The function raises an error if the input is
    invalid or not supported.

    :param option_type: The input option type, either as an OptionType enum value or a string.
    :type option_type: Union[str, OptionType]
    :return: The corresponding QuantLib option type (ql.Option.Call or ql.Option.Put).
    :rtype: ql.Option
    :raises ValueError: If the input option type is invalid or not supported.
    :raises TypeError: If the input type is not a valid OptionType enum value or a string.

    Example usage:

    >>> convert_option_type_to_ql(OptionType.CALL)
    <OptionType.Call: 1>
    >>> convert_option_type_to_ql('put')
    <OptionType.Put: -1>
    """
    if isinstance(option_type, str):
        option_type = option_type.upper()
        if option_type not in OptionType.__members__:
            raise ValueError(f"Invalid option type \"{option_type}\", expected one of "
                             f"{list(OptionType.__members__.keys())}")
        return convert_option_type_to_ql(OptionType[option_type])
    elif isinstance(option_type, OptionType):
        if option_type == OptionType.CALL:
            return ql.Option.Call
        elif option_type == OptionType.PUT:
            return ql.Option.Put
        else:
            raise ValueError(f"Invalid option type \"{option_type}\"")
    else:
        raise TypeError(
            f"Invalid input type {type(option_type)} for option type")


class OptionTypeField(fields.Field):
    def _serialize(self, value: OptionType, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> OptionType:
        try:
            return OptionType[value]
        except KeyError as error:
            raise ValidationError(f"Invalid option type \"{value}\", expected one of "
                                  f"{list(OptionType.__members__.keys())}") from error
