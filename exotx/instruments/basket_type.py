from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class BasketType(Enum):
    MINBASKET = 'minbasket'
    MAXBASKET = 'maxbasket'
    SPREADBASKET = 'spreadbasket'
    AVERAGEBASKET = 'averagebasket'


def convert_basket_type(basket_type: Union[str, BasketType]) -> BasketType:
    """
    Converts the input basket_type to a BasketType enumeration value.

    :param basket_type: A string or BasketType instance representing the basket type.
    :type basket_type: Union[str, BasketType]
    :return: The corresponding BasketType enumeration value.
    :rtype: BasketType
    :raises ValueError: If the input string is not a valid BasketType member.
    :raises Exception: If the input is neither a string nor a BasketType instance.

    Example usage:

    >>> convert_basket_type("minbasket")
    <BasketType.MINBASKET: 1>
    >>> convert_basket_type(BasketType.MINBASKET)
    <BasketType.MINBASKET: 1>
    """
    if isinstance(basket_type, str):
        basket_type = basket_type.upper()
        if basket_type not in BasketType.__members__:
            raise ValueError(
                f"Invalid basket type \"{basket_type}\", expected one of {list(BasketType.__members__.keys())}")
        return BasketType[basket_type]
    elif isinstance(basket_type, BasketType):
        return basket_type
    else:
        raise Exception(f"Invalid basket type \"{type(basket_type)}\"")


class BasketTypeField(fields.Field):
    def _serialize(self, value: BasketType, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> BasketType:
        try:
            return BasketType[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid basket type \"{value}\", expected one of {list(BasketType.__members__.keys())}") from error
