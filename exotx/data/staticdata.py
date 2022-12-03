import json
import QuantLib as ql
from typing import Union
from exotx.data.static.daycounters import day_counters_to_ql, DayCounter
from exotx.data.static.calendar import Calendar, CalendarSchema
from exotx.data.static.calendars import calendars_to_ql_calendars
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

    # region Day counter
    @staticmethod
    def get_default_day_counter() -> DayCounter:
        return DayCounter.Actual360

    def _set_day_counter(self, day_counter: Union[DayCounter, str, None]) -> None:
        if isinstance(day_counter, DayCounter):
            self.day_counter = day_counter
        elif isinstance(day_counter, str):
            try:
                self.day_counter = DayCounter[day_counter]
            except KeyError as err:
                raise ValueError(f"Invalid day counter \'{day_counter}\'") from err
        elif day_counter is None:
            self.day_counter: DayCounter = self.get_default_day_counter()
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
    def get_default_calendar() -> Calendar:
        return Calendar.get_default_calendar()

    @staticmethod
    def get_ql_default_calendar() -> ql.Calendar:
        return ql.TARGET()

    def get_ql_calendar(self) -> ql.Calendar:
        if self.calendar.region:
            # TODO: Make sure market is defined as CalendarMarket.Settlement here if market was None
            return calendars_to_ql_calendars[self.calendar.region][self.calendar.market]
        else:
            return self.get_ql_default_calendar()

    def _set_calendar(self, value: Union[Calendar, dict, None]) -> None:
        if isinstance(value, Calendar):
            self.calendar = value
        elif isinstance(value, dict):
            if 'region' in value.keys():
                region = value['region']
                assert region in list(calendars_to_ql_calendars.keys()), f"Invalid region \'{region}\'"
                if 'market' in value.keys():
                    market = value['market']
                    assert market in list(calendars_to_ql_calendars[
                                              region].keys()), f"Invalid market \'{market}\' for region \'{region}\'"
                    self.calendar = Calendar(region=region, market=market)
                else:
                    # set calendar with default market
                    self.calendar = Calendar(region=region, market=None)
            else:
                if 'market' in value.keys():
                    raise Exception(f"Missing calendar for market \'{value['market']}\'")
                else:
                    # set default calendar
                    self.calendar = self.get_default_calendar()
        elif value is None:
            self.calendar = self.get_default_calendar()
        else:
            raise ValueError(f"Invalid calendar type {type(value)}")

    # endregion

    # region Business day convention
    @staticmethod
    def get_default_business_day_convention() -> BusinessDayConvention:
        return BusinessDayConvention.ModifiedFollowing

    def get_default_ql_business_day_convention(self) -> int:
        return business_day_conventions_to_ql[self.business_day_convention]

    def _set_business_day_convention(self, value: Union[BusinessDayConvention, str, None]) -> None:
        if isinstance(value, BusinessDayConvention):
            self.business_day_convention = value
        elif isinstance(value, str):
            try:
                self.business_day_convention = BusinessDayConvention[value]
            except KeyError as err:
                raise ValueError(f"Invalid business day convention \'{value}\'") from err
        elif value is None:
            self.business_day_convention = self.get_default_business_day_convention()
        else:
            raise ValueError(f"Invalid business day convention type {type(value)}")

    # endregion

    @staticmethod
    def from_json(data: dict):
        schema = StaticDataSchema()
        return schema.load(data)

    def to_json(self, format_type: str = "dict"):
        schema = StaticDataSchema()
        my_json = schema.dump(self)
        if format_type == "dict":
            return my_json
        elif format_type == "str":
            return json.dumps(my_json)
        else:
            raise NotImplemented(f"Invalid format type {format_type} when dumping")


class BusinessDayConventionField(fields.Field):
    def _serialize(self, value: BusinessDayConvention, attr, obj, **kwargs) -> str:
        return value.name

    def _deserialize(self, value: str, attr, data, **kwargs) -> BusinessDayConvention:
        try:
            if value:
                return BusinessDayConvention[value]
            else:
                return StaticData.get_default_business_day_convention()
        except KeyError as error:
            raise ValidationError(f"Invalid business day convention \'{value}\'") from error


class DayCounterField(fields.Field):
    def _serialize(self, value: DayCounter, attr, obj, **kwargs) -> str:
        return value.name

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
