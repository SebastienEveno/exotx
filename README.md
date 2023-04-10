# exotx

<p align="center">
    <img src="https://github.com/SebastienEveno/exotx/actions/workflows/python-package.yml/badge.svg?branch=master" />
    <a href="https://pypi.org/project/exotx" alt="Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/exotx.svg?logo=python&logoColor=white" /></a>
    <a href="https://pypi.org/project/exotx" alt="PyPi">
        <img src="https://img.shields.io/pypi/v/exotx" /></a>
    <a href="https://pepy.tech/project/exotx" alt="Downloads">
        <img src="https://pepy.tech/badge/exotx" /></a>
</p>

exotx is a Python wrapper for the [QuantLib library](https://www.quantlib.org/), a powerful open-source library for
quantitative finance. exotx provides a simple and user-friendly interface for pricing and analyzing financial
derivatives using QuantLib's advanced numerical methods.

## Installation

To install exotx, simply use pip:

```sh
pip install exotx
```

## Usage

### Define the product

```python
import exotx

notional = 100
strike = 100.0
autocall_barrier_level = 1.0  # 100%
annual_coupon_value = 0.03  # 3.00%
coupon_barrier_level = 0.75  # 75%
protection_barrier_level = 0.75  # 75%

my_autocallable = exotx.Autocallable(notional, strike, autocall_barrier_level, annual_coupon_value, coupon_barrier_level, protection_barrier_level)
```

### Define the static data

The object that represents static data such as the calendar, the day counter or the business day convention used.

#### From the constructor

```python
my_static_data = exotx.StaticData(day_counter='Actual360', business_day_convention='ModifiedFollowing')
```

#### From JSON

```python
my_json = {
    'day_counter': 'Actual360',
    'business_day_convention': 'ModifiedFollowing'
}
my_static_data = exotx.StaticData.from_json(my_json)
```

### Define the market data

#### From the constructor

```python
reference_date = '2015-11-06'
spot = 100.0
risk_free_rate = 0.01
dividend_rate = 0.0
black_scholes_volatility = 0.2

my_market_data = exotx.MarketData(reference_date, spot, risk_free_rate, dividend_rate, black_scholes_volatility=black_scholes_volatility)
```

#### From JSON

```python
my_json = {
    'reference_date': '2015-11-06',
    'spot': 100,
    'risk_free_rate': 0.01,
    'dividend_rate': 0,
    'black_scholes_volatility': 0.2
}
my_market_data = exotx.MarketData.from_json(my_json)
```

### Price the product

```python
exotx.price(my_autocallable, my_market_data, my_static_data, model='black-scholes')
```

```plaintext
96.08517973497098
```

## Contributing

We welcome contributions to exotx! If you find a bug or would like to request a new feature, please open an issue on
the [Github repository](https://github.com/sebastieneveno/exotx).
If you would like to contribute code, please submit a pull request.

## License

exotx is released under the [MIT License](https://opensource.org/licenses/MIT).
