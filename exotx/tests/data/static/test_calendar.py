import pytest
from exotx.data.static import Calendar, CalendarRegion, CalendarMarket
from typing import Optional, Union


# region from_json
@pytest.mark.parametrize('region, market', [
    ('UnitedStates', 'NYSE'),
    (CalendarRegion.UnitedStates, CalendarMarket.NYSE),
    (CalendarRegion.UnitedStates, None)
])
def test_calendar_from_json(region: Union[CalendarRegion, str, None], market: Union[CalendarMarket, str, None]):
    # Arrange
    if isinstance(region, str):
        my_region = region
    elif isinstance(region, CalendarRegion):
        my_region = region.name
    else:
        my_region = None

    if isinstance(market, str):
        my_market = market
    elif isinstance(market, CalendarMarket):
        my_market = market.name
    else:
        my_market = None

    my_json = {
        'region': my_region,
        'market': my_market
    }

    # Act
    my_calendar = Calendar.from_json(my_json)

    # Assert
    assert isinstance(my_calendar.region, CalendarRegion)
    assert isinstance(my_calendar.market, CalendarMarket)
    if region:
        if isinstance(region, str):
            assert my_calendar.region.name == region
        else:
            assert my_calendar.region == region
        if market:
            if isinstance(market, str):
                assert my_calendar.market.name == market
            else:
                assert my_calendar.market == market
        else:
            assert my_calendar.market == CalendarMarket.Settlement
    else:
        assert my_calendar.region is None
        assert my_calendar.market is None


@pytest.mark.parametrize('region', [
    'UnitedStates'
])
def test_calendar_from_json_default_market(region: Union[CalendarRegion, str, None]):
    # Arrange
    my_json = {
        'region': region
    }

    # Act
    my_calendar = Calendar.from_json(my_json)

    # Assert
    assert isinstance(my_calendar.region, CalendarRegion)
    if isinstance(region, str):
        assert my_calendar.region.name == region
    elif isinstance(region, CalendarRegion):
        assert my_calendar.region == region
    assert my_calendar.market == CalendarMarket.Settlement


@pytest.mark.parametrize('market', [
    'NYSE'
])
def test_calendar_from_json_missing_region_for_market(market: Optional[str]):
    # Arrange
    my_json = {
        'market': market
    }

    # Act
    with pytest.raises(Exception) as e:
        _ = Calendar.from_json(my_json)

    # Assert
    assert str(e.value) == f'Missing region for market \'{market}\''


@pytest.mark.parametrize('region, market', [
    ('UnitedState', 'NYSE')  # Invalid region
])
def test_calendar_from_json_invalid_region(region: Optional[str], market: Optional[str]):
    # Arrange
    my_json = {
        'region': region,
        'market': market,
    }

    # Act
    with pytest.raises(Exception) as e:
        _ = Calendar.from_json(my_json)

    # Assert
    assert str(e.value) == f'Invalid region \'{region}\'. Available regions: Argentina, Australia, BespokeCalendar, ' \
                           f'Brazil, Canada, China, CzechRepublic, Denmark, Finland, France, Germany, HongKong, ' \
                           f'Hungary, Iceland, India, Indonesia, Israel, Italy, Japan, Mexico, NewZealand, Norway, ' \
                           f'NullCalendar, Poland, Romania, Russia, SaudiArabia, Singapore, Slovakia, SouthAfrica, ' \
                           f'SouthKorea, Sweden, Switzerland, Taiwan, TARGET, Thailand, Turkey, Ukraine, UnitedKingdom, ' \
                           f'UnitedStates, WeekendsOnly'


@pytest.mark.parametrize('region, market', [
    ('UnitedStates', 'whatever')  # Invalid market for that region
])
def test_calendar_from_json_invalid_market_for_region(region: Optional[str], market: Optional[str]):
    # Arrange
    my_json = {
        'region': region,
        'market': market,
    }

    # Act
    with pytest.raises(Exception) as e:
        _ = Calendar.from_json(my_json)

    # Assert
    assert str(e.value) == f'Invalid market \'{market}\' for region \'{region}\'. Available markets: Settlement, ' \
                           f'FederalReserve, GovernmentBond, LiborImpact, NERC, NYSE'


# endregion


# region to_json
@pytest.mark.parametrize('region, market', [
    ('UnitedStates', 'NYSE'),
    (CalendarRegion.UnitedStates, CalendarMarket.NYSE),
    (CalendarRegion.UnitedStates, None)
])
def test_calendar_to_json(region: Union[CalendarRegion, str, None], market: Union[CalendarMarket, str, None]):
    # Arrange
    my_calendar = Calendar(region=region, market=market)

    # Act
    my_json = my_calendar.to_json()

    # Assert
    if isinstance(region, str):
        assert my_json['region'] == region
    elif isinstance(region, CalendarRegion):
        assert my_json['region'] == region.name
    if market is None:
        assert my_json['market'] == 'Settlement'
    else:
        if isinstance(market, str):
            assert my_json['market'] == market
        elif isinstance(market, CalendarMarket):
            assert my_json['market'] == market.name

# endregion
