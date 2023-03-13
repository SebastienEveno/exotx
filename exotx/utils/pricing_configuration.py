from marshmallow import Schema, fields, ValidationError, post_load

from exotx.enums.enums import PricingModel, NumericalMethod, RandomNumberGenerator


class PricingConfiguration:
    def __init__(self, model: PricingModel, numerical_method: NumericalMethod,
                 random_number_generator: RandomNumberGenerator = RandomNumberGenerator.PSEUDORANDOM,
                 compute_greeks: bool = False):
        self.model = model
        self.numerical_method = numerical_method
        self.compute_greeks = compute_greeks
        self.random_number_generator = random_number_generator

    def to_json(self):
        return PricingConfigurationSchema().dump(self)

    @classmethod
    def from_json(cls, json_data):
        return PricingConfigurationSchema().load(json_data)


# region Schema

class PricingModelField(fields.Field):
    def _serialize(self, value: PricingModel, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> PricingModel:
        try:
            return PricingModel[value]
        except KeyError as error:
            raise ValidationError(f"Invalid pricing model \'{value}\'") from error


class NumericalMethodField(fields.Field):
    def _serialize(self, value: NumericalMethod, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> NumericalMethod:
        try:
            return NumericalMethod[value]
        except KeyError as error:
            raise ValidationError(f"Invalid numerical method \'{value}\'") from error


class RandomNumberGeneratorField(fields.Field):
    def _serialize(self, value: RandomNumberGenerator, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> RandomNumberGenerator:
        try:
            return RandomNumberGenerator[value]
        except KeyError as error:
            raise ValidationError(f"Invalid random number generator \'{value}\'") from error


class PricingConfigurationSchema(Schema):
    model = PricingModelField(allow_none=False)
    numerical_method = NumericalMethodField(allow_none=False)
    compute_greeks = fields.Boolean()
    random_number_generator = RandomNumberGeneratorField(allow_none=True)

    @post_load
    def make_pricing_configuration(self, data, **kwargs) -> PricingConfiguration:
        return PricingConfiguration(**data)

# endregion
