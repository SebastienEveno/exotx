from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class AverageConvention(Enum):
    PRICE = 'price'
    STRIKE = 'strike'


def convert_average_convention(average_convention: Union[str, AverageConvention]) -> AverageConvention:
    if isinstance(average_convention, str):
        average_convention = average_convention.upper()
        if average_convention not in AverageConvention.__members__:
            raise ValueError(
                f"Invalid average convention \"{average_convention}\", expected one of {list(AverageConvention.__members__.keys())}")
        return AverageConvention[average_convention]
    elif isinstance(average_convention, AverageConvention):
        return average_convention
    else:
        raise Exception(f"Invalid average convention type \"{type(average_convention)}\"")


class AverageConventionField(fields.Field):
    def _serialize(self, value: AverageConvention, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageConvention:
        try:
            return AverageConvention[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average convention \"{value}\", expected one of {list(AverageConvention.__members__.keys())}") from error
