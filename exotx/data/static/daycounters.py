import QuantLib as ql

# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#daycounter
day_counters = {
    'SimpleDayCounter': ql.SimpleDayCounter(),
    'Thirty360': ql.Thirty360(),
    'Actual360': ql.Actual360(),
    'Actual365Fixed': ql.Actual365Fixed(),
    'Actual365Fixed(Canadian)': ql.Actual365Fixed(ql.Actual365Fixed.Canadian),
    'Actual365FixedNoLeap': ql.Actual365Fixed(ql.Actual365Fixed.NoLeap),
    'ActualActual': ql.ActualActual(),
    'Business252': ql.Business252()
}
