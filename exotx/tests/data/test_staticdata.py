import QuantLib as ql
import pytest
from typing import Optional
from exotx.data import StaticData


# Arrange
def my_default_day_counter_type() -> type:
    my_default_day_counter = StaticData.get_default_day_counter()
    return type(my_default_day_counter)


def my_default_calendar_type() -> type:
    my_default_calendar = StaticData.get_default_calendar()
    return type(my_default_calendar)


def my_default_business_day_convention_type() -> type:
    my_default_business_day_convention = StaticData.get_default_business_day_convention()
    return type(my_default_business_day_convention)


@pytest.mark.parametrize('day_counter, expected_parent_class_type, expected_class_type', [
                             ('Actual360', ql.DayCounter, ql.Actual360),
                             ('SimpleDayCounter', ql.DayCounter, ql.SimpleDayCounter),
                             ('Thirty360', ql.DayCounter, ql.Thirty360),
                             ('Actual365Fixed', ql.DayCounter, ql.Actual365Fixed),
                             ('Actual365Fixed(Canadian)', ql.DayCounter, ql.Actual365Fixed),
                             ('Actual365FixedNoLeap', ql.DayCounter, ql.Actual365Fixed),
                             ('ActualActual', ql.DayCounter, ql.ActualActual),
                             ('Business252', ql.DayCounter, ql.Business252),
                             (None, ql.DayCounter, my_default_day_counter_type())  # default behavior
                         ])
def test_static_data_day_counter(day_counter: Optional[str],
                                 expected_parent_class_type: type,
                                 expected_class_type: type) -> None:
    # Act
    my_static_data = StaticData(day_counter=day_counter)

    # Assert
    assert isinstance(my_static_data.day_counter, expected_parent_class_type)
    assert isinstance(my_static_data.day_counter, expected_class_type)

    # default settings
    assert isinstance(my_static_data.calendar, my_default_calendar_type())
    assert isinstance(my_static_data.business_day_convention, my_default_business_day_convention_type())


@pytest.mark.parametrize('day_counter', [
                             'actual360',  # wrong day counter
                         ])
def test_static_data_day_counter_invalid_day_counter(day_counter: Optional[str]) -> None:
    # Act
    with pytest.raises(Exception) as e:
        _ = StaticData(day_counter=day_counter)

    # Assert
    assert str(e.value) == f'Invalid day counter \'{day_counter}\''


@pytest.mark.parametrize('calendar, market, expected_parent_class_type, expected_class_type', [
                             ('Argentina', 'Merval', ql.Calendar, ql.Argentina),
                             ('Argentina', 'default', ql.Calendar, ql.Argentina),
                             ('Argentina', None, ql.Calendar, ql.Argentina),
                             ('Australia', 'default', ql.Calendar, ql.Australia),
                             ('Australia', None, ql.Calendar, ql.Australia),
                             ('BespokeCalendar', 'default', ql.Calendar, ql.BespokeCalendar),
                             ('BespokeCalendar', None, ql.Calendar, ql.BespokeCalendar),
                             ('Brazil', 'Exchange', ql.Calendar, ql.Brazil),
                             ('Brazil', 'Settlement', ql.Calendar, ql.Brazil),
                             ('Brazil', 'default', ql.Calendar, ql.Brazil),
                             ('Brazil', None, ql.Calendar, ql.Brazil),
                             ('Canada', 'Settlement', ql.Calendar, ql.Canada),
                             ('Canada', 'TSX', ql.Calendar, ql.Canada),
                             ('Canada', 'default', ql.Calendar, ql.Canada),
                             ('Canada', None, ql.Calendar, ql.Canada),
                             ('China', 'IB', ql.Calendar, ql.China),
                             ('China', 'SSE', ql.Calendar, ql.China),
                             ('China', 'default', ql.Calendar, ql.China),
                             ('China', None, ql.Calendar, ql.China),
                             ('CzechRepublic', 'PSE', ql.Calendar, ql.CzechRepublic),
                             ('CzechRepublic', 'default', ql.Calendar, ql.CzechRepublic),
                             ('CzechRepublic', None, ql.Calendar, ql.CzechRepublic),
                             ('Denmark', 'default', ql.Calendar, ql.Denmark),
                             ('Finland', 'default', ql.Calendar, ql.Finland),
                             ('France', 'Exchange', ql.Calendar, ql.France),
                             ('France', 'Settlement', ql.Calendar, ql.France),
                             ('France', 'default', ql.Calendar, ql.France),
                             ('Germany', 'Eurex', ql.Calendar, ql.Germany),
                             ('Germany', 'FrankfurtStockExchange', ql.Calendar, ql.Germany),
                             ('Germany', 'Settlement', ql.Calendar, ql.Germany),
                             ('Germany', 'Xetra', ql.Calendar, ql.Germany),
                             ('Germany', 'default', ql.Calendar, ql.Germany),
                             ('Germany', None, ql.Calendar, ql.Germany),
                             ('HongKong', 'HKEx', ql.Calendar, ql.HongKong),
                             ('HongKong', 'default', ql.Calendar, ql.HongKong),
                             ('HongKong', None, ql.Calendar, ql.HongKong),
                             ('Hungary', 'default', ql.Calendar, ql.Hungary),
                             ('Hungary', None, ql.Calendar, ql.Hungary),
                             ('Iceland', 'ICEX', ql.Calendar, ql.Iceland),
                             ('Iceland', 'default', ql.Calendar, ql.Iceland),
                             ('Iceland', None, ql.Calendar, ql.Iceland),
                             ('India', 'NSE', ql.Calendar, ql.India),
                             ('India', 'default', ql.Calendar, ql.India),
                             ('India', None, ql.Calendar, ql.India),
                             ('Indonesia', 'BEJ', ql.Calendar, ql.Indonesia),
                             ('Indonesia', 'JSX', ql.Calendar, ql.Indonesia),
                             ('Indonesia', 'default', ql.Calendar, ql.Indonesia),
                             ('Indonesia', None, ql.Calendar, ql.Indonesia),
                             ('Israel', 'Settlement', ql.Calendar, ql.Israel),
                             ('Israel', 'TASE', ql.Calendar, ql.Israel),
                             ('Israel', 'default', ql.Calendar, ql.Israel),
                             ('Israel', None, ql.Calendar, ql.Israel),
                             ('Italy', 'Exchange', ql.Calendar, ql.Italy),
                             ('Italy', 'Settlement', ql.Calendar, ql.Italy),
                             ('Italy', 'default', ql.Calendar, ql.Italy),
                             ('Italy', None, ql.Calendar, ql.Italy),
                             ('Japan', 'default', ql.Calendar, ql.Japan),
                             ('Japan', None, ql.Calendar, ql.Japan),
                             ('Mexico', 'BMV', ql.Calendar, ql.Mexico),
                             ('Mexico', None, ql.Calendar, ql.Mexico),
                             ('NewZealand', 'default', ql.Calendar, ql.NewZealand),
                             ('NewZealand', None, ql.Calendar, ql.NewZealand),
                             ('Norway', 'default', ql.Calendar, ql.Norway),
                             ('Norway', None, ql.Calendar, ql.Norway),
                             ('NullCalendar', 'default', ql.Calendar, ql.NullCalendar),
                             ('NullCalendar', None, ql.Calendar, ql.NullCalendar),
                             ('Poland', 'default', ql.Calendar, ql.Poland),
                             ('Poland', None, ql.Calendar, ql.Poland),
                             ('Romania', 'default', ql.Calendar, ql.Romania),
                             ('Romania', None, ql.Calendar, ql.Romania),
                             ('Russia', 'MOEX', ql.Calendar, ql.Russia),
                             ('Russia', 'Settlement', ql.Calendar, ql.Russia),
                             ('Russia', 'default', ql.Calendar, ql.Russia),
                             ('Russia', None, ql.Calendar, ql.Russia),
                             ('SaudiArabia', 'Tadawul', ql.Calendar, ql.SaudiArabia),
                             ('SaudiArabia', 'default', ql.Calendar, ql.SaudiArabia),
                             ('SaudiArabia', None, ql.Calendar, ql.SaudiArabia),
                             ('Singapore', 'SGX', ql.Calendar, ql.Singapore),
                             ('Singapore', 'default', ql.Calendar, ql.Singapore),
                             ('Singapore', None, ql.Calendar, ql.Singapore),
                             ('Slovakia', 'BSSE', ql.Calendar, ql.Slovakia),
                             ('Slovakia', 'default', ql.Calendar, ql.Slovakia),
                             ('Slovakia', None, ql.Calendar, ql.Slovakia),
                             ('SouthAfrica', 'default', ql.Calendar, ql.SouthAfrica),
                             ('SouthAfrica', None, ql.Calendar, ql.SouthAfrica),
                             ('SouthKorea', 'KRX', ql.Calendar, ql.SouthKorea),
                             ('SouthKorea', 'Settlement', ql.Calendar, ql.SouthKorea),
                             ('SouthKorea', 'default', ql.Calendar, ql.SouthKorea),
                             ('SouthKorea', None, ql.Calendar, ql.SouthKorea),
                             ('Sweden', 'default', ql.Calendar, ql.Sweden),
                             ('Sweden', None, ql.Calendar, ql.Sweden),
                             ('Switzerland', 'default', ql.Calendar, ql.Switzerland),
                             ('Switzerland', None, ql.Calendar, ql.Switzerland),
                             ('Taiwan', 'TSEC', ql.Calendar, ql.Taiwan),
                             ('Taiwan', 'default', ql.Calendar, ql.Taiwan),
                             ('Taiwan', None, ql.Calendar, ql.Taiwan),
                             ('TARGET', 'default', ql.Calendar, ql.TARGET),
                             ('TARGET', None, ql.Calendar, ql.TARGET),
                             ('Thailand', 'default', ql.Calendar, ql.Thailand),
                             ('Thailand', None, ql.Calendar, ql.Thailand),
                             ('Turkey', 'default', ql.Calendar, ql.Turkey),
                             ('Turkey', None, ql.Calendar, ql.Turkey),
                             ('Ukraine', 'USE', ql.Calendar, ql.Ukraine),
                             ('Ukraine', 'default', ql.Calendar, ql.Ukraine),
                             ('Ukraine', None, ql.Calendar, ql.Ukraine),
                             ('UnitedKingdom', 'Exchange', ql.Calendar, ql.UnitedKingdom),
                             ('UnitedKingdom', 'Metals', ql.Calendar, ql.UnitedKingdom),
                             ('UnitedKingdom', 'Settlement', ql.Calendar, ql.UnitedKingdom),
                             ('UnitedKingdom', 'default', ql.Calendar, ql.UnitedKingdom),
                             ('UnitedKingdom', None, ql.Calendar, ql.UnitedKingdom),
                             ('UnitedStates', 'FederalReserve', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'GovernmentBond', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'LiborImpact', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'NERC', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'NYSE', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'Settlement', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', 'default', ql.Calendar, ql.UnitedStates),
                             ('UnitedStates', None, ql.Calendar, ql.UnitedStates),
                             ('WeekendsOnly', 'default', ql.Calendar, ql.WeekendsOnly),
                             ('WeekendsOnly', None, ql.Calendar, ql.WeekendsOnly),
                             (None, None, ql.Calendar, my_default_calendar_type())  # default behavior
                         ])
def test_static_data_calendar_ok(calendar: Optional[str], market: Optional[str],
                                 expected_parent_class_type: type,
                                 expected_class_type: type) -> None:
    # Act
    my_static_data = StaticData(calendar=calendar, market=market)

    # Assert
    assert isinstance(my_static_data.calendar, expected_parent_class_type)
    assert isinstance(my_static_data.calendar, expected_class_type)

    # default settings
    assert isinstance(my_static_data.day_counter, my_default_day_counter_type())
    assert isinstance(my_static_data.business_day_convention, my_default_business_day_convention_type())


@pytest.mark.parametrize('calendar, market', [
                             ('argentina', 'whatever'),  # wrong calendar
                         ])
def test_static_data_calendar_invalid_calendar(calendar: Optional[str], market: Optional[str]) -> None:
    # Act
    with pytest.raises(Exception) as e:
        _ = StaticData(calendar=calendar, market=market)

    # Assert
    assert str(e.value) == f'Invalid calendar \'{calendar}\''


@pytest.mark.parametrize('calendar, market', [
                             ('Argentina', 'market'),  # wrong market name
                         ])
def test_static_data_calendar_invalid_market(calendar: Optional[str], market: Optional[str]) -> None:
    # Act
    with pytest.raises(Exception) as e:
        _ = StaticData(calendar=calendar, market=market)

    # Assert
    assert str(e.value) == f'Invalid market \'{market}\' for calendar \'{calendar}\''


@pytest.mark.parametrize('calendar, market', [
                             (None, 'default')  # market provided but no calendar
                         ])
def test_static_data_calendar_market_provided_but_no_calendar(calendar: Optional[str], market: Optional[str]) -> None:
    # Act
    with pytest.raises(Exception) as e:
        _ = StaticData(calendar=calendar, market=market)

    # Assert
    assert str(e.value) == f'Missing calendar for market \'{market}\''
