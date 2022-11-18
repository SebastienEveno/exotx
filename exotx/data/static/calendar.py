from typing import Union
from marshmallow import Schema, fields, post_load, ValidationError
from exotx.data.static.calendars import CalendarRegion, CalendarMarket, region_to_markets


class Calendar:
    def __init__(self,
                 region: Union[CalendarRegion, str, None] = None,
                 market: Union[CalendarMarket, str, None] = None):
        if region:
            if isinstance(region, str):
                try:
                    self.region = CalendarRegion[region]
                except KeyError as err:
                    available_regions = [region.name for region in CalendarRegion]
                    raise ValueError(f"Invalid region \'{region}\'. Available regions: {', '.join(available_regions)}") from err
            elif isinstance(region, CalendarRegion):
                self.region = region
            else:
                raise TypeError(f"Invalid type for region \'{region}\'")
            if market:
                if isinstance(market, str):
                    try:
                        calendar_market = CalendarMarket[market]
                        self._check_market_with_respect_to_region(self.region, calendar_market)
                    except KeyError as err:
                        available_markets = [market.name for market in region_to_markets[self.region]]
                        raise ValueError(f"Invalid market \'{market}\' for region \'{region}\'. Available markets: {', '.join(available_markets)}") from err
                elif isinstance(market, CalendarMarket):
                    self._check_market_with_respect_to_region(self.region, market)
                else:
                    raise TypeError(f"Invalid type for market")
            else:
                # set default market
                self.market = CalendarMarket.Settlement
        else:
            if market:
                if isinstance(market, str):
                    raise ValueError(f"Missing region for market \'{market}\'")
                elif isinstance(market, CalendarMarket):
                    raise ValueError(f"Missing region for market \'{market.value}\'")
                else:
                    raise TypeError(f"Invalid type for market")
            else:
                # set default market
                self.region = None
                self.market = None

    def _check_market_with_respect_to_region(self, region: CalendarRegion, market: CalendarMarket):
        if market not in region_to_markets[self.region]:
            raise ValueError(f"Invalid market \'{market.name}\' for region \'{region.name}\'")
        self.market = market

    @staticmethod
    def get_default_calendar():
        return Calendar(region=None, market=None)

    @staticmethod
    def from_json(data: dict):
        schema = CalendarSchema()
        return schema.load(data)


class CalendarRegionField(fields.Field):

    def _deserialize(self, value: str, attr, data, **kwargs) -> CalendarRegion:
        try:
            if value:
                return CalendarRegion[value]
        except KeyError as error:
            raise ValidationError(f"Invalid region \'{value}\'") from error


class CalendarMarketField(fields.Field):

    def _deserialize(self, value: str, attr, data, **kwargs) -> CalendarMarket:
        try:
            if value:
                return CalendarMarket[value]
        except KeyError as error:
            raise ValidationError(f"Invalid region \'{value}\'") from error


class CalendarSchema(Schema):
    region = fields.Str(allow_none=True)
    market = fields.Str(allow_none=True)

    @post_load
    def make_calendar(self, data, **kwargs) -> Calendar:
        return Calendar(**data)
