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

exotx allows you to easily price exotic options with a couple of lines of Python code.

It is based on [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance.

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
```python
my_static_data = exotx.StaticData()
```

### Define the market data
```python
reference_date = '2015-11-06'
spot = 100.0
risk_free_rate = 0.01
dividend_rate = 0.0
black_scholes_volatility = 0.2

my_market_data = exotx.MarketData(reference_date, spot, risk_free_rate, dividend_rate, black_scholes_volatility=black_scholes_volatility)
```

### Price the product
```python
my_autocallable.price(my_market_data, my_static_data, model='black-scholes')
```
```plaintext
96.08517973497098
```
