from typing import Union, Tuple
from marshmallow import Schema, fields, post_load, validates_schema
from exotx.data.static.calendars import CalendarRegion, CalendarMarket, region_to_markets, available_regions


class Calendar:
    def __init__(self,
                 region: Union[CalendarRegion, str, None] = None,
                 market: Union[CalendarMarket, str, None] = None):
        self.region, self.market = Calendar.validate_inputs(region, market)

    @staticmethod
    def validate_inputs(region, market) -> Tuple[Union[CalendarRegion, None], Union[CalendarMarket, None]]:
        if region:
            if isinstance(region, str):
                try:
                    region = CalendarRegion[region]
                except KeyError as err:
                    raise ValueError(
                        f"Invalid region \'{region}\'. Available regions: {', '.join(available_regions)}") from err
            elif isinstance(region, CalendarRegion):
                pass
            else:
                raise TypeError(f"Invalid type for region \'{region.__repr__()}\'")
            if market:
                if isinstance(market, str):
                    try:
                        market = CalendarMarket[market]
                    except KeyError as err:
                        available_markets = [market.name for market in region_to_markets[region]]
                        raise ValueError(
                            f"Invalid market \'{market}\' for region \'{region.name}\'. Available markets: {', '.join(available_markets)}") from err
                Calendar.check_market_with_respect_to_region(region, market)
            else:
                # set default market
                market = CalendarMarket.Settlement
        else:
            if market:
                if isinstance(market, str):
                    raise ValueError(f"Missing region for market \'{market}\'")
                elif isinstance(market, CalendarMarket):
                    raise ValueError(f"Missing region for market \'{market.name}\'")
                else:
                    raise TypeError(f"Invalid type for market")
            else:
                # set default market
                region = None
                market = None

        return region, market

    @staticmethod
    def check_market_with_respect_to_region(region: CalendarRegion, market: CalendarMarket):
        if market not in region_to_markets[region]:
            available_markets = [market.name for market in region_to_markets[region]]
            raise ValueError(
                f"Invalid market \'{market.name}\' for region \'{region.name}\'. Available markets: {', '.join(available_markets)}")

    @staticmethod
    def get_default_calendar():
        return Calendar(region=None, market=None)

    @staticmethod
    def from_json(data: dict):
        schema = CalendarSchema()
        return schema.load(data)

    def to_json(self):
        schema = CalendarSchema()
        return schema.dump(self)


class CalendarRegionField(fields.Field):
    def _serialize(self, value: CalendarRegion, attr, obj, **kwargs) -> str:
        if value is not None:
            return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> str:
        return value


class CalendarMarketField(fields.Field):
    def _serialize(self, value: CalendarMarket, attr, obj, **kwargs) -> str:
        if value is not None:
            return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> str:
        return value


class CalendarSchema(Schema):
    region = CalendarRegionField(allow_none=True)
    market = CalendarMarketField(allow_none=True)

    @validates_schema
    def validate_region_and_market(self, data, **kwargs):
        if 'region' in data:
            if 'market' in data:
                _ = Calendar.validate_inputs(data['region'], data['market'])
            else:
                _ = Calendar.validate_inputs(data['region'], None)
        else:
            _ = Calendar.validate_inputs(None, data['market'])

    @post_load
    def make_calendar(self, data, **kwargs) -> Calendar:
        return Calendar(**data)
