import enum

import QuantLib as ql

# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#calendar


class CalendarRegion(enum.Enum):
    Argentina = 0
    Australia = 1
    BespokeCalendar = 2  # TODO: to be removed?
    Brazil = 3
    Canada = 4
    China = 5
    CzechRepublic = 6
    Denmark = 7
    Finland = 8
    France = 9
    Germany = 10
    HongKong = 11
    Hungary = 12
    Iceland = 13
    India = 14
    Indonesia = 15
    Israel = 16
    Italy = 17
    Japan = 18
    Mexico = 19
    NewZealand = 20
    Norway = 21
    NullCalendar = 22  # TODO: to be removed?
    Poland = 23
    Romania = 24
    Russia = 25
    SaudiArabia = 26
    Singapore = 27
    Slovakia = 28
    SouthAfrica = 29
    SouthKorea = 30
    Sweden = 31
    Switzerland = 32
    Taiwan = 33
    Thailand = 34
    Turkey = 35
    Ukraine = 36
    UnitedKingdom = 37
    UnitedStates = 38
    WeekendsOnly = 39  # TODO: to be removed?


class CalendarMarket(enum.Enum):
    Settlement = 0
    Merval = 1
    Exchange = 2
    TSX = 3
    IB = 4
    SSE = 5
    PSE = 6
    Eurex = 7
    FrankfurtStockExchange = 8
    Xetra = 9
    HKEx = 10
    ICEX = 11
    NSE = 12
    BEJ = 13
    JSX = 14
    TASE = 15
    BMV = 16
    MOEX = 17
    Tadawul = 18
    SGX = 19
    BSSE = 20
    KRX = 21
    TSEC = 22
    USE = 23
    Metals = 24
    FederalReserve = 25
    GovernmentBond = 26
    LiborImpact = 27
    NERC = 28
    NYSE = 29


region_to_markets = {
    CalendarRegion.Argentina: [
        CalendarMarket.Settlement,
        CalendarMarket.Merval
    ],
    CalendarRegion.Australia: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.BespokeCalendar: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Brazil: [
        CalendarMarket.Settlement,
        CalendarMarket.Exchange
    ],
    CalendarRegion.Canada: [
        CalendarMarket.Settlement,
        CalendarMarket.TSX
    ],
    CalendarRegion.China: [
        CalendarMarket.Settlement,
        CalendarMarket.IB,
        CalendarMarket.SSE
    ],
    CalendarRegion.CzechRepublic: [
        CalendarMarket.Settlement,
        CalendarMarket.PSE
    ],
    CalendarRegion.Denmark: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Finland: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.France: [
        CalendarMarket.Settlement,
        CalendarMarket.Exchange
    ],
    CalendarRegion.Germany: [
        CalendarMarket.Settlement,
        CalendarMarket.Eurex,
        CalendarMarket.FrankfurtStockExchange,
        CalendarMarket.Xetra
    ],
    CalendarRegion.HongKong: [
        CalendarMarket.Settlement,
        CalendarMarket.HKEx
    ],
    CalendarRegion.Hungary: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Iceland: [
        CalendarMarket.Settlement,
        CalendarMarket.ICEX
    ],
    CalendarRegion.India: [
        CalendarMarket.Settlement,
        CalendarMarket.NSE
    ],
    CalendarRegion.Indonesia: [
        CalendarMarket.Settlement,
        CalendarMarket.BEJ,
        CalendarMarket.JSX
    ],
    CalendarRegion.Israel: [
        CalendarMarket.Settlement,
        CalendarMarket.TASE
    ],
    CalendarRegion.Italy: [
        CalendarMarket.Settlement,
        CalendarMarket.Exchange
    ],
    CalendarRegion.Japan: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Mexico: [
        CalendarMarket.Settlement,
        CalendarMarket.BMV
    ],
    CalendarRegion.NewZealand: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Norway: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.NullCalendar: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Poland: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Romania: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Russia: [
        CalendarMarket.Settlement,
        CalendarMarket.MOEX
    ],
    CalendarRegion.SaudiArabia: [
        CalendarMarket.Settlement,
        CalendarMarket.Tadawul
    ],
    CalendarRegion.Singapore: [
        CalendarMarket.Settlement,
        CalendarMarket.SGX
    ],
    CalendarRegion.Slovakia: [
        CalendarMarket.Settlement,
        CalendarMarket.BSSE
    ],
    CalendarRegion.SouthAfrica: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.SouthKorea: [
        CalendarMarket.Settlement,
        CalendarMarket.KRX
    ],
    CalendarRegion.Sweden: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Switzerland: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Taiwan: [
        CalendarMarket.Settlement,
        CalendarMarket.TSEC
    ],
    CalendarRegion.Thailand: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Turkey: [
        CalendarMarket.Settlement
    ],
    CalendarRegion.Ukraine: [
        CalendarMarket.Settlement,
        CalendarMarket.USE
    ],
    CalendarRegion.UnitedKingdom: [
        CalendarMarket.Settlement,
        CalendarMarket.Exchange,
        CalendarMarket.Metals
    ],
    CalendarRegion.UnitedStates: [
        CalendarMarket.Settlement,
        CalendarMarket.FederalReserve,
        CalendarMarket.GovernmentBond,
        CalendarMarket.LiborImpact,
        CalendarMarket.NERC,
        CalendarMarket.NYSE
    ],
    CalendarRegion.WeekendsOnly: [
        CalendarMarket.Settlement
    ]
}

calendars = {
    CalendarRegion.Argentina: {
        CalendarMarket.Merval: ql.Argentina(ql.Argentina.Merval),
        CalendarMarket.Settlement: ql.Argentina()
    },
    CalendarRegion.Australia: {
        CalendarMarket.Settlement: ql.Australia()
    },
    'BespokeCalendar': {
        'Default': ql.BespokeCalendar('BespokeCalendar')
    },
    'Brazil': {
        'Exchange': ql.Brazil(ql.Brazil.Exchange),
        'Settlement': ql.Brazil(ql.Brazil.Settlement),
        'Default': ql.Brazil()
    },
    'Canada': {
        'Settlement': ql.Canada(ql.Canada.Settlement),
        'TSX': ql.Canada(ql.Canada.TSX),
        'Default': ql.Canada()
    },
    'China': {
        'IB': ql.China(ql.China.IB),
        'SSE': ql.China(ql.China.SSE),
        'Default': ql.China()
    },
    'CzechRepublic': {
        'PSE': ql.CzechRepublic(ql.CzechRepublic.PSE),
        'Default': ql.CzechRepublic()
    },
    'Denmark': {
        'Default': ql.Denmark()
    },
    'Finland': {
        'Default': ql.Finland()
    },
    'France': {
        'Exchange': ql.France(ql.France.Exchange),
        'Settlement': ql.France(ql.France.Settlement),
        'Default': ql.France()
    },
    'Germany': {
        'Eurex': ql.Germany(ql.Germany.Eurex),
        'FrankfurtStockExchange': ql.Germany(ql.Germany.FrankfurtStockExchange),
        'Settlement': ql.Germany(ql.Germany.Settlement),
        'Xetra': ql.Germany(ql.Germany.Xetra),
        'Default': ql.Germany()
    },
    'HongKong': {
        'HKEx': ql.HongKong(ql.HongKong.HKEx),
        'Default': ql.HongKong()
    },
    'Hungary': {
        'Default': ql.Hungary()
    },
    'Iceland': {
        'ICEX': ql.Iceland(ql.Iceland.ICEX),
        'Default': ql.Iceland()
    },
    'India': {
        'NSE': ql.India(ql.India.NSE),
        'Default': ql.India()
    },
    'Indonesia': {
        'BEJ': ql.Indonesia(ql.Indonesia.BEJ),
        'JSX': ql.Indonesia(ql.Indonesia.JSX),
        'Default': ql.Indonesia()
    },
    'Israel': {
        'Settlement': ql.Israel(ql.Israel.Settlement),
        'TASE': ql.Israel(ql.Israel.TASE),
        'Default': ql.Israel()
    },
    'Italy': {
        'Exchange': ql.Italy(ql.Italy.Exchange),
        'Settlement': ql.Italy(ql.Italy.Settlement),
        'Default': ql.Italy()
    },
    'Japan': {
        'Default': ql.Japan()
    },
    'Mexico': {
        'BMV': ql.Mexico(ql.Mexico.BMV),
        'Default': ql.Mexico()
    },
    'NewZealand': {
        'Default': ql.NewZealand()
    },
    'Norway': {
        'Default': ql.Norway()
    },
    'NullCalendar': {
        'Default': ql.NullCalendar()
    },
    'Poland': {
        'Default': ql.Poland()
    },
    'Romania': {
        'Default': ql.Romania()
    },
    'Russia': {
        'MOEX': ql.Russia(ql.Russia.MOEX),
        'Settlement': ql.Russia(ql.Russia.Settlement),
        'Default': ql.Russia()
    },
    'SaudiArabia': {
        'Tadawul': ql.SaudiArabia(ql.SaudiArabia.Tadawul),
        'Default': ql.SaudiArabia()
    },
    'Singapore': {
        'SGX': ql.Singapore(ql.Singapore.SGX),
        'Default': ql.Singapore()
    },
    'Slovakia': {
        'BSSE': ql.Slovakia(ql.Slovakia.BSSE),
        'Default': ql.Slovakia()
    },
    'SouthAfrica': {
        'Default': ql.SouthAfrica()
    },
    'SouthKorea': {
        'KRX': ql.SouthKorea(ql.SouthKorea.KRX),
        'Settlement': ql.SouthKorea(ql.SouthKorea.Settlement),
        'Default': ql.SouthKorea()
    },
    'Sweden': {
        'Default': ql.Sweden()
    },
    'Switzerland': {
        'Default': ql.Switzerland()
    },
    'Taiwan': {
        'TSEC': ql.Taiwan(ql.Taiwan.TSEC),
        'Default': ql.Taiwan()
    },
    'TARGET': {
        'Default': ql.TARGET()
    },
    'Thailand': {
        'Default': ql.Thailand()
    },
    'Turkey': {
        'Default': ql.Turkey()
    },
    'Ukraine': {
        'USE': ql.Ukraine(ql.Ukraine.USE),
        'Default': ql.Ukraine()
    },
    'UnitedKingdom': {
        'Exchange': ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
        'Metals': ql.UnitedKingdom(ql.UnitedKingdom.Metals),
        'Settlement': ql.UnitedKingdom(ql.UnitedKingdom.Settlement),
        'Default': ql.UnitedKingdom()
    },
    'UnitedStates': {
        'FederalReserve': ql.UnitedStates(ql.UnitedStates.FederalReserve),
        'GovernmentBond': ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        'LiborImpact': ql.UnitedStates(ql.UnitedStates.LiborImpact),
        'NERC': ql.UnitedStates(ql.UnitedStates.NERC),
        'NYSE': ql.UnitedStates(ql.UnitedStates.NYSE),
        'Settlement': ql.UnitedStates(ql.UnitedStates.Settlement),
        'Default': ql.UnitedStates()
    },
    'WeekendsOnly': {
        'Default': ql.WeekendsOnly()
    }
}
