from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class BasketType(Enum):
    MINBASKET = 'minbasket'
    MAXBASKET = 'maxbasket'
    SPREADBASKET = 'spreadbasket'
    AVERAGEBASKET = 'averagebasket'


def convert_basket_type(basket_type: Union[str, BasketType]) -> BasketType:
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
