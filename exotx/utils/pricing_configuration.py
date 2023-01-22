from exotx.enums.enums import PricingModelEnum, NumericalMethodEnum
from marshmallow import Schema, fields, ValidationError, post_load


class PricingConfiguration:
    def __init__(self, model: PricingModelEnum, numerical_method: NumericalMethodEnum, compute_greeks: bool):
        self.model = model
        self.numerical_method = numerical_method
        self.compute_greeks = compute_greeks

    def to_json(self):
        return PricingConfigurationSchema().dump(self)

    @classmethod
    def from_json(cls, json_data):
        return PricingConfigurationSchema().load(json_data)


# region Schema

class PricingModelField(fields.Field):
    def _serialize(self, value: PricingModelEnum, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> PricingModelEnum:
        try:
            return PricingModelEnum[value]
        except KeyError as error:
            raise ValidationError(f"Invalid pricing model \'{value}\'") from error


class NumericalMethodField(fields.Field):
    def _serialize(self, value: NumericalMethodEnum, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> NumericalMethodEnum:
        try:
            return NumericalMethodEnum[value]
        except KeyError as error:
            raise ValidationError(f"Invalid numerical method \'{value}\'") from error


class PricingConfigurationSchema(Schema):
    model = PricingModelField(allow_none=False)
    numerical_method = NumericalMethodField(allow_none=False)
    compute_greeks = fields.Boolean()

    @post_load
    def make_pricing_configuration(self, data, **kwargs) -> PricingConfiguration:
        return PricingConfiguration(**data)

# endregion
