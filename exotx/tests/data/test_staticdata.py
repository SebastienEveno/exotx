import QuantLib as ql
import pytest
from typing import Optional, Union
from exotx.data import StaticData
from exotx.data.static import Calendar, BusinessDayConvention, DayCounter


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


# region DayCounter
@pytest.mark.parametrize('day_counter, expected_class_type, expected_ql_class_type', [
    ('Actual360', DayCounter, ql.Actual360),
    ('SimpleDayCounter', DayCounter, ql.SimpleDayCounter),
    ('Thirty360', DayCounter, ql.Thirty360),
    ('Actual365Fixed', DayCounter, ql.Actual365Fixed),
    ('Actual365FixedCanadian', DayCounter, ql.Actual365Fixed),
    ('Actual365FixedNoLeap', DayCounter, ql.Actual365Fixed),
    ('ActualActual', DayCounter, ql.ActualActual),
    ('Business252', DayCounter, ql.Business252),
    (None, DayCounter, ql.Actual360)  # default behavior
])
def test_static_data_day_counter(day_counter: Optional[str],
                                 expected_class_type: type,
                                 expected_ql_class_type: type) -> None:
    # Act
    my_static_data = StaticData(day_counter=day_counter)

    # Assert
    assert isinstance(my_static_data.day_counter, expected_class_type)
    assert isinstance(my_static_data.get_ql_day_counter(), expected_ql_class_type)

    # default settings
    assert isinstance(my_static_data.calendar, my_default_calendar_type())
    assert isinstance(my_static_data.business_day_convention, my_default_business_day_convention_type())


@pytest.mark.parametrize('day_counter', [
    'actual360',  # invalid day counter
])
def test_static_data_invalid_day_counter(day_counter: Optional[str]) -> None:
    # Act
    with pytest.raises(Exception) as e:
        _ = StaticData(day_counter=day_counter)

    # Assert
    assert str(e.value) == f'Invalid day counter \'{day_counter}\''


# endregion DayCounter

# region Calendar
@pytest.mark.parametrize('region, market, expected_class_type, expected_ql_class_type', [
    ('Argentina', 'Merval', Calendar, ql.Argentina),
    ('Argentina', 'Settlement', Calendar, ql.Argentina),
    ('Argentina', None, Calendar, ql.Argentina),
    ('Australia', 'Settlement', Calendar, ql.Australia),
    ('Australia', None, Calendar, ql.Australia),
    ('BespokeCalendar', 'Settlement', Calendar, ql.BespokeCalendar),
    ('BespokeCalendar', None, Calendar, ql.BespokeCalendar),
    ('Brazil', 'Exchange', Calendar, ql.Brazil),
    ('Brazil', 'Settlement', Calendar, ql.Brazil),
    ('Brazil', None, Calendar, ql.Brazil),
    ('Canada', 'Settlement', Calendar, ql.Canada),
    ('Canada', 'TSX', Calendar, ql.Canada),
    ('Canada', None, Calendar, ql.Canada),
    ('China', 'IB', Calendar, ql.China),
    ('China', 'SSE', Calendar, ql.China),
    ('China', 'Settlement', Calendar, ql.China),
    ('China', None, Calendar, ql.China),
    ('CzechRepublic', 'PSE', Calendar, ql.CzechRepublic),
    ('CzechRepublic', 'Settlement', Calendar, ql.CzechRepublic),
    ('CzechRepublic', None, Calendar, ql.CzechRepublic),
    ('Denmark', 'Settlement', Calendar, ql.Denmark),
    ('Finland', 'Settlement', Calendar, ql.Finland),
    ('France', 'Exchange', Calendar, ql.France),
    ('France', 'Settlement', Calendar, ql.France),
    ('Germany', 'Eurex', Calendar, ql.Germany),
    ('Germany', 'FrankfurtStockExchange', Calendar, ql.Germany),
    ('Germany', 'Settlement', Calendar, ql.Germany),
    ('Germany', 'Xetra', Calendar, ql.Germany),
    ('Germany', None, Calendar, ql.Germany),
    ('HongKong', 'HKEx', Calendar, ql.HongKong),
    ('HongKong', 'Settlement', Calendar, ql.HongKong),
    ('HongKong', None, Calendar, ql.HongKong),
    ('Hungary', 'Settlement', Calendar, ql.Hungary),
    ('Hungary', None, Calendar, ql.Hungary),
    ('Iceland', 'ICEX', Calendar, ql.Iceland),
    ('Iceland', 'Settlement', Calendar, ql.Iceland),
    ('Iceland', None, Calendar, ql.Iceland),
    ('India', 'NSE', Calendar, ql.India),
    ('India', 'Settlement', Calendar, ql.India),
    ('India', None, Calendar, ql.India),
    ('Indonesia', 'BEJ', Calendar, ql.Indonesia),
    ('Indonesia', 'JSX', Calendar, ql.Indonesia),
    ('Indonesia', 'Settlement', Calendar, ql.Indonesia),
    ('Indonesia', None, Calendar, ql.Indonesia),
    ('Israel', 'Settlement', Calendar, ql.Israel),
    ('Israel', 'TASE', Calendar, ql.Israel),
    ('Israel', None, Calendar, ql.Israel),
    ('Italy', 'Exchange', Calendar, ql.Italy),
    ('Italy', 'Settlement', Calendar, ql.Italy),
    ('Italy', None, Calendar, ql.Italy),
    ('Japan', 'Settlement', Calendar, ql.Japan),
    ('Japan', None, Calendar, ql.Japan),
    ('Mexico', 'BMV', Calendar, ql.Mexico),
    ('Mexico', None, Calendar, ql.Mexico),
    ('NewZealand', 'Settlement', Calendar, ql.NewZealand),
    ('NewZealand', None, Calendar, ql.NewZealand),
    ('Norway', 'Settlement', Calendar, ql.Norway),
    ('Norway', None, Calendar, ql.Norway),
    ('NullCalendar', 'Settlement', Calendar, ql.NullCalendar),
    ('NullCalendar', None, Calendar, ql.NullCalendar),
    ('Poland', 'Settlement', Calendar, ql.Poland),
    ('Poland', None, Calendar, ql.Poland),
    ('Romania', 'Settlement', Calendar, ql.Romania),
    ('Romania', None, Calendar, ql.Romania),
    ('Russia', 'MOEX', Calendar, ql.Russia),
    ('Russia', 'Settlement', Calendar, ql.Russia),
    ('Russia', None, Calendar, ql.Russia),
    ('SaudiArabia', 'Tadawul', Calendar, ql.SaudiArabia),
    ('SaudiArabia', 'Settlement', Calendar, ql.SaudiArabia),
    ('SaudiArabia', None, Calendar, ql.SaudiArabia),
    ('Singapore', 'SGX', Calendar, ql.Singapore),
    ('Singapore', 'Settlement', Calendar, ql.Singapore),
    ('Singapore', None, Calendar, ql.Singapore),
    ('Slovakia', 'BSSE', Calendar, ql.Slovakia),
    ('Slovakia', 'Settlement', Calendar, ql.Slovakia),
    ('Slovakia', None, Calendar, ql.Slovakia),
    ('SouthAfrica', 'Settlement', Calendar, ql.SouthAfrica),
    ('SouthAfrica', None, Calendar, ql.SouthAfrica),
    ('SouthKorea', 'KRX', Calendar, ql.SouthKorea),
    ('SouthKorea', 'Settlement', Calendar, ql.SouthKorea),
    ('SouthKorea', None, Calendar, ql.SouthKorea),
    ('Sweden', 'Settlement', Calendar, ql.Sweden),
    ('Sweden', None, Calendar, ql.Sweden),
    ('Switzerland', 'Settlement', Calendar, ql.Switzerland),
    ('Switzerland', None, Calendar, ql.Switzerland),
    ('Taiwan', 'TSEC', Calendar, ql.Taiwan),
    ('Taiwan', 'Settlement', Calendar, ql.Taiwan),
    ('Taiwan', None, Calendar, ql.Taiwan),
    ('TARGET', 'Settlement', Calendar, ql.TARGET),
    ('TARGET', None, Calendar, ql.TARGET),
    ('Thailand', 'Settlement', Calendar, ql.Thailand),
    ('Thailand', None, Calendar, ql.Thailand),
    ('Turkey', 'Settlement', Calendar, ql.Turkey),
    ('Turkey', None, Calendar, ql.Turkey),
    ('Ukraine', 'USE', Calendar, ql.Ukraine),
    ('Ukraine', 'Settlement', Calendar, ql.Ukraine),
    ('Ukraine', None, Calendar, ql.Ukraine),
    ('UnitedKingdom', 'Exchange', Calendar, ql.UnitedKingdom),
    ('UnitedKingdom', 'Metals', Calendar, ql.UnitedKingdom),
    ('UnitedKingdom', 'Settlement', Calendar, ql.UnitedKingdom),
    ('UnitedKingdom', None, Calendar, ql.UnitedKingdom),
    ('UnitedStates', 'FederalReserve', Calendar, ql.UnitedStates),
    ('UnitedStates', 'GovernmentBond', Calendar, ql.UnitedStates),
    ('UnitedStates', 'LiborImpact', Calendar, ql.UnitedStates),
    ('UnitedStates', 'NERC', Calendar, ql.UnitedStates),
    ('UnitedStates', 'NYSE', Calendar, ql.UnitedStates),
    ('UnitedStates', 'Settlement', Calendar, ql.UnitedStates),
    ('UnitedStates', None, Calendar, ql.UnitedStates),
    ('WeekendsOnly', 'Settlement', Calendar, ql.WeekendsOnly),
    ('WeekendsOnly', None, Calendar, ql.WeekendsOnly),
    (None, None, Calendar, ql.TARGET)  # default behavior
])
def test_static_data_calendar(region: Optional[str], market: Optional[str],
                              expected_class_type: type,
                              expected_ql_class_type: type) -> None:
    # Arrange
    my_calendar = Calendar(region=region, market=market)

    # Act
    my_static_data = StaticData(calendar=my_calendar)

    # Assert
    assert isinstance(my_static_data.calendar, expected_class_type)
    assert isinstance(my_static_data.get_ql_calendar(), expected_ql_class_type)

    # default settings
    assert isinstance(my_static_data.day_counter, my_default_day_counter_type())
    assert isinstance(my_static_data.business_day_convention, my_default_business_day_convention_type())


# endregion Calendar

# region BusinessDayConvention
@pytest.mark.parametrize('business_day_convention, expected_class_type, expected_ql_value', [
    ('Following', BusinessDayConvention, ql.Following),
    ('ModifiedFollowing', BusinessDayConvention, ql.ModifiedFollowing),
    ('Preceding', BusinessDayConvention, ql.Preceding),
    ('ModifiedPreceding', BusinessDayConvention, ql.ModifiedPreceding),
    ('Unadjusted', BusinessDayConvention, ql.Unadjusted),
    (None, BusinessDayConvention, ql.ModifiedFollowing)  # default behavior
])
def test_static_data_business_day_convention(business_day_convention: Optional[str],
                                             expected_class_type: type,
                                             expected_ql_value: int):
    # Act
    my_static_data = StaticData(business_day_convention=business_day_convention)

    # Assert
    assert isinstance(my_static_data.business_day_convention, expected_class_type)
    assert my_static_data.get_default_ql_business_day_convention() == expected_ql_value

    # default settings
    assert isinstance(my_static_data.day_counter, my_default_day_counter_type())
    assert isinstance(my_static_data.calendar, my_default_calendar_type())


@pytest.mark.parametrize('business_day_convention', [
    'Followin'  # invalid business day convention
])
def test_static_data_invalid_business_day_convention(business_day_convention: Optional[str]):
    with pytest.raises(Exception) as e:
        _ = StaticData(business_day_convention=business_day_convention)

    # Assert
    assert str(e.value) == f'Invalid business day convention \'{business_day_convention}\''


# endregion

# region from_json
def test_static_data_from_json():
    # Arrange
    my_json = {
        'day_counter': 'Actual360',
        'calendar': {
            'region': 'UnitedStates',
            'market': 'NYSE',
        },
        'business_day_convention': 'ModifiedFollowing'
    }

    # Act
    my_static_data = StaticData.from_json(my_json)

    # Assert
    assert isinstance(my_static_data.business_day_convention, BusinessDayConvention)
    assert isinstance(my_static_data.day_counter, DayCounter)
    assert isinstance(my_static_data.calendar, Calendar)


# endregion

# region to_json

@pytest.mark.parametrize('day_counter, business_day_convention, region, market', [
    ('Actual360', 'Following', 'UnitedStates', 'Settlement'),
    (None, None, None, None)
])
def test_static_data_to_json(day_counter: Union[str, None], business_day_convention: Union[str, None],
                             region: Union[str, None], market: Union[str, None]):
    # Arrange
    my_calendar = Calendar(region=region, market=market)
    my_static_data = StaticData(day_counter=day_counter, business_day_convention=business_day_convention,
                                calendar=my_calendar)

    # Act
    my_json = my_static_data.to_json()

    # Assert
    assert isinstance(my_json, dict)
    assert 'day_counter' in my_json
    assert 'calendar' in my_json
    assert 'business_day_convention' in my_json
    if day_counter is None:
        assert my_json['day_counter'] == StaticData.get_default_day_counter().name
    else:
        assert my_json['day_counter'] == day_counter
    if business_day_convention is None:
        assert my_json['business_day_convention'] == StaticData.get_default_business_day_convention().name
    else:
        assert my_json['business_day_convention'] == business_day_convention
    assert my_json['calendar']['region'] == region
    assert my_json['calendar']['market'] == market

# endregion
