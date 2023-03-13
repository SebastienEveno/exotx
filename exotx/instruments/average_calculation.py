from enum import Enum
from typing import Union

from marshmallow import fields, ValidationError


class AverageCalculation(Enum):
    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'


def convert_average_calculation(average_calculation: Union[str, AverageCalculation]) -> AverageCalculation:
    if isinstance(average_calculation, str):
        average_calculation = average_calculation.upper()
        if average_calculation not in AverageCalculation.__members__:
            raise ValueError(
                f"Invalid average calculation \"{average_calculation}\", expected one of {list(AverageCalculation.__members__.keys())}")
        return AverageCalculation[average_calculation]
    elif isinstance(average_calculation, AverageCalculation):
        return average_calculation
    else:
        raise Exception(f"Invalid average calculation type \"{type(average_calculation)}\"")


class AverageCalculationField(fields.Field):
    def _serialize(self, value: AverageCalculation, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> AverageCalculation:
        try:
            return AverageCalculation[value]
        except KeyError as error:
            raise ValidationError(
                f"Invalid average calculation \"{value}\", expected one of {list(AverageCalculation.__members__.keys())}") from error
