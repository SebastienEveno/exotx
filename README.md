# exotx
<p align="center">
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
strike = 100.0  # equal to the spot price
autocall_barrier_level = 1.0  # 100%
annual_coupon_value = 0.03  # 3.00%
coupon_barrier_level = 0.75  # 75%
protection_barrier_level = 0.75  # 75%

my_autocallable = exotx.Autocallable(notional, strike, autocall_barrier_level, annual_coupon_value, coupon_barrier_level, protection_barrier_level)
```

### Define the market data
```python
import datetime

reference_date = datetime.datetime(2022, 6, 5)
spot = 100.0
risk_free_rate = 0.01
dividend_rate = 0.0
black_scholes_volatility = 0.2

my_market_data = exotx.MarketData(reference_date, spot, risk_free_rate, dividend_rate, black_scholes_volatility=black_scholes_volatility)
```

### Price the product
```python
my_autocallable.price(reference_date, my_market_data, model='black-scholes')
```
```plaintext
96.15395623462899
```
