from datetime import datetime

from exotx.data.marketdata import MarketData


def test_market_data_from_json():
    # Arrange
    my_json = {
        'reference_date': '2015-11-06',
        'underlying_spots': [100],
        'risk_free_rate': 0.01,
        'dividend_rate': 0,
        'underlying_black_scholes_volatilities': [0.2]
    }

    # Act
    my_market_data = MarketData.from_json(my_json)

    # Assert
    assert isinstance(my_market_data.reference_date, datetime)
