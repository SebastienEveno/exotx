import enum
import QuantLib as ql


# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#conventions


# region Compounding
class Compounding(enum.Enum):
    Simple = 0
    Compounded = 1
    Continuous = 2
    SimpleThenCompounded = 3
    CompoundedThenSimple = 4


compoundings = {
    'Simple': ql.Simple,
    'Compounded': ql.Compounded,
    'Continuous': ql.Continuous,
    'SimpleThenCompounded': ql.SimpleThenCompounded,
    'CompoundedThenSimple': ql.CompoundedThenSimple
}


# endregion


# region Frequencies
class Frequencies(enum.Enum):
    NoFrequency = 0,
    Once = 1
    Annual = 2
    Semiannual = 3
    EveryFourthMonth = 4
    Quarterly = 5
    Bimonthly = 6
    Monthly = 7
    EveryFourthWeek = 8
    Biweekly = 9
    Weekly = 10
    Daily = 11


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


# endregion


# region Business day convention
class BusinessDayConvention(enum.Enum):
    Following = 0
    ModifiedFollowing = 1
    Preceding = 2
    ModifiedPreceding = 3
    Unadjusted = 4


business_day_conventions_to_ql = {
    BusinessDayConvention.Following: ql.Following,
    BusinessDayConvention.ModifiedFollowing: ql.ModifiedFollowing,
    BusinessDayConvention.Preceding: ql.Preceding,
    BusinessDayConvention.ModifiedPreceding: ql.ModifiedPreceding,
    BusinessDayConvention.Unadjusted: ql.Unadjusted
}
# endregion
