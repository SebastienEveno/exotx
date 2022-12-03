import enum
import QuantLib as ql


# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#daycounter


class DayCounter(enum.Enum):
    SimpleDayCounter = 0
    Thirty360 = 1
    Actual360 = 2
    Actual365Fixed = 3
    Actual365FixedCanadian = 4
    Actual365FixedNoLeap = 5
    ActualActual = 6
    Business252 = 7


day_counters_to_ql = {
    DayCounter.SimpleDayCounter: ql.SimpleDayCounter(),
    DayCounter.Thirty360: ql.Thirty360(),
    DayCounter.Actual360: ql.Actual360(),
    DayCounter.Actual365Fixed: ql.Actual365Fixed(),
    DayCounter.Actual365FixedCanadian: ql.Actual365Fixed(ql.Actual365Fixed.Canadian),
    DayCounter.Actual365FixedNoLeap: ql.Actual365Fixed(ql.Actual365Fixed.NoLeap),
    DayCounter.ActualActual: ql.ActualActual(),
    DayCounter.Business252: ql.Business252()
}
