import QuantLib as ql

# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#conventions

compoundings = {
    'Simple': ql.Simple,
    'Compounded': ql.Compounded,
    'Continuous': ql.Continuous,
    'SimpleThenCompounded': ql.SimpleThenCompounded,
    'CompoundedThenSimple': ql.CompoundedThenSimple
}

frequencies = {
    'NoFrequency': ql.NoFrequency,
    'Once': ql.Once,
    'Annual': ql.Annual,
    'Semiannual': ql.Semiannual,
    'EveryFourthMonth': ql.EveryFourthMonth,
    'Quarterly': ql.Quarterly,
    'Bimonthly': ql.Bimonthly,
    'Monthly': ql.Monthly,
    'EveryFourthWeek': ql.EveryFourthWeek,
    'Biweekly': ql.Biweekly,
    'Weekly': ql.Weekly,
    'Daily': ql.Daily
}

business_day_conventions = {
    'Following': ql.Following,
    'ModifiedFollowing': ql.ModifiedFollowing,
    'Preceding': ql.Preceding,
    'ModifiedPreceding': ql.ModifiedPreceding,
    'Unadjusted': ql.Unadjusted
}