import QuantLib as ql
from typing import Optional
from exotx.data.static.daycounters import day_counters
from exotx.data.static.calendars import calendars
from exotx.data.static.conventions import business_day_conventions


class StaticData(object):
    def __init__(self,
                 day_counter: Optional[str] = None,
                 calendar: Optional[str] = None,
                 market: Optional[str] = None,
                 business_day_convention: Optional[str] = None) -> None:
        self.default_market_name = 'default'
        self._set_day_counter(day_counter)
        self._set_calendar(calendar, market)
        self._set_business_day_convention(business_day_convention)

    # region Day counter
    @staticmethod
    def get_default_day_counter() -> ql.DayCounter:
        return ql.Actual360()

    def _set_day_counter(self, day_counter: Optional[str]) -> None:
        if day_counter:
            assert day_counter in list(day_counters.keys()), f"Invalid day counter \'{day_counter}\'"
            self.day_counter: ql.DayCounter = day_counters[day_counter]
        else:
            # set default day counter
            self.day_counter: ql.DayCounter = self.get_default_day_counter()

    # endregion

    # region Calendar
    @staticmethod
    def get_default_calendar() -> ql.Calendar:
        return ql.TARGET()

    def _set_calendar(self, calendar: Optional[str], market: Optional[str]) -> None:
        if calendar:
            assert calendar in list(calendars.keys()), f"Invalid calendar \'{calendar}\'"
            if market:
                assert market in list(calendars[calendar].keys()), f"Invalid market \'{market}\' for calendar \'{calendar}\'"
                self.calendar: ql.Calendar = calendars[calendar][market]
            else:
                # set calendar with default market
                self.calendar: ql.Calendar = calendars[calendar][self.default_market_name]
        else:
            if market:
                raise Exception(f"Missing calendar for market \'{market}\'")
            else:
                # set default calendar
                self.calendar: ql.Calendar = self.get_default_calendar()

    # endregion

    # region Business day convention
    @staticmethod
    def get_default_business_day_convention() -> int:
        return ql.ModifiedFollowing

    def _set_business_day_convention(self, business_day_convention: Optional[str]) -> None:
        if business_day_convention:
            assert business_day_convention in list(business_day_conventions.keys()), f"Invalid weekday correction \'{business_day_convention}\'"
            self.business_day_convention: int = business_day_conventions[business_day_convention]
        else:
            self.business_day_convention: int = ql.ModifiedFollowing

    # endregion
