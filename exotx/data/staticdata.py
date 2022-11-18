import QuantLib as ql
from typing import Optional, Union
from exotx.data.static.daycounters import day_counters_to_ql, DayCounter
from exotx.data.static.calendar import Calendar, CalendarSchema
from exotx.data.static.calendars import calendars
from exotx.data.static.conventions import business_day_conventions_to_ql, BusinessDayConvention
from marshmallow import Schema, fields, post_load, ValidationError


class StaticData:
    def __init__(self,
                 day_counter: Union[DayCounter, str, None] = None,
                 business_day_convention: Union[BusinessDayConvention, str, None] = None,
                 calendar: Union[Calendar, dict, None] = None) -> None:
        # day counter
        self._set_day_counter(day_counter)

        # business day convention
        self._set_business_day_convention(business_day_convention)

        # calendar
        self._set_calendar(calendar)
        # self.calendar = calendar
        # if calendar:
        #     self._set_calendar(calendar['region'], calendar['market'])

    # region Day counter
    @staticmethod
    def get_default_day_counter() -> DayCounter:
        return DayCounter.Actual360

    def _set_day_counter(self, day_counter: Union[DayCounter, str, None]) -> None:
        if isinstance(day_counter, DayCounter):
            self.day_counter = day_counter
        elif isinstance(day_counter, str):
            try:
                if day_counter:
                    self.day_counter = DayCounter[day_counter]
                    # self.day_counter: ql.DayCounter = day_counters_to_ql[day_counter]
                else:
                    # set default day counter
                    self.day_counter: DayCounter = self.get_default_day_counter()
            except KeyError as err:
                raise ValueError(f"Invalid day counter \'{day_counter}\'") from err
        else:
            raise ValueError(f"Invalid day counter type {type(day_counter)}")

    def get_ql_day_counter(self) -> ql.DayCounter:
        return day_counters_to_ql[self.day_counter]

    @staticmethod
    def get_ql_default_day_counter():
        return day_counters_to_ql[StaticData.get_default_day_counter()]

    # endregion

    # region Calendar
    @staticmethod
    def _get_default_calendar() -> Calendar:
        return Calendar.get_default_calendar()

    @staticmethod
    def get_ql_default_calendar() -> ql.Calendar:
        return ql.TARGET()

    def get_ql_calendar(self) -> ql.Calendar:
        if self.calendar.region:
            # TODO: Make sure market is defined as CalendarMarket.Settlement here if market was None
            return calendars[self.calendar.region][self.calendar.market]
        else:
            return self.get_ql_default_calendar()

    def _set_calendar(self, value: Union[Calendar, dict, None]) -> None:
        if isinstance(value, Calendar):
            self.calendar = value
        elif isinstance(value, dict):
            if 'region' in value.keys():
                region = value['region']
                assert region in list(calendars.keys()), f"Invalid region \'{region}\'"
                if 'market' in value.keys():
                    market = value['market']
                    assert market in list(calendars[region].keys()), f"Invalid market \'{market}\' for region \'{region}\'"
                    self.calendar: Calendar(region=region, market=market)
                else:
                    # set calendar with default market
                    self.calendar: Calendar(region=region, market=None)
            else:
                if 'market' in value.keys():
                    raise Exception(f"Missing calendar for market \'{value['market']}\'")
                else:
                    # set default calendar
                    self.calendar = self._get_default_calendar()
        else:
            raise ValueError(f"Invalid calendar type {type(value)}")

    # endregion

    # region Business day convention
    @staticmethod
    def get_default_business_day_convention() -> BusinessDayConvention:
        return BusinessDayConvention.ModifiedFollowing
        # return ql.ModifiedFollowing

    def _set_business_day_convention(self, value: Union[BusinessDayConvention, str, None]) -> None:
        if isinstance(value, BusinessDayConvention):
            self.business_day_convention = value
        elif isinstance(value, str):
            try:
                if value:
                    self.business_day_convention = BusinessDayConvention[value]
                else:
                    self.business_day_convention = self.get_default_business_day_convention()
            except KeyError as err:
                raise ValueError(f"Invalid business day convention \'{value}\'")
        else:
            raise ValueError(f"Invalid business day convention type {type(value)}")

    # endregion

    @staticmethod
    def from_json(data: dict):
        schema = StaticDataSchema()
        return schema.load(data)

    # def to_json(self):
    #     schema = StaticDataSchema()
    #     return schema.dump(self)


# class CalendarField(fields.Field):
#     # def _serialize(self, value, attr, obj, **kwargs):
#     #     if value is None:
#     #         return None
#     #     return dict(Region=value['region'], market=value['market'])
#
#     def _deserialize(self, value, attr, data, **kwargs):
#         if value:
#             if value['region']:
#                 region = value['region']
#                 if region not in list(calendars.keys()):
#                     raise ValidationError("Invalid region \'{region}\'")
#                 if value['market']:
#                     market = value['market']
#                     if market not in list(calendars[region].keys()):
#                         raise ValidationError("Invalid market \'{market}\' for region \'{region}\'")
#                     return calendars[region][market]
#                 else:
#                     # set calendar with default market
#                     return calendars[region]['Default']
#             else:
#                 if value['market']:
#                     raise ValidationError(f"Missing region for market \'{value['market']}\'")
#                 return StaticData.get_default_calendar()
#         # default value
#         return StaticData.get_default_calendar()


class BusinessDayConventionField(fields.Field):
    # def _serialize(self, value: BusinessDayConvention, attr, obj, **kwargs) -> str:
    #     return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> BusinessDayConvention:
        try:
            if value:
                return BusinessDayConvention[value]
            else:
                return StaticData.get_default_business_day_convention()
        except KeyError as error:
            raise ValidationError(f"Invalid business day convention \'{value}\'") from error


class DayCounterField(fields.Field):
    # def _serialize(self, value: DayCounter, attr, obj, **kwargs) -> str:
    #     return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> DayCounter:
        try:
            if value:
                return DayCounter[value]
            else:
                return StaticData.get_default_day_counter()
        except KeyError as error:
            raise ValidationError(f"Invalid day counter \'{value}\'") from error


class StaticDataSchema(Schema):
    day_counter = DayCounterField(allow_none=True)
    business_day_convention = BusinessDayConventionField(allow_none=True)
    calendar = fields.Nested(CalendarSchema(), allow_none=True)

    @post_load
    def make_static_data(self, data, **kwargs) -> StaticData:
        return StaticData(**data)
