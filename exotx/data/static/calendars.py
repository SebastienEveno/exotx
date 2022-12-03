import enum

import QuantLib as ql


# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#calendar


class CalendarRegion(enum.Enum):
    Argentina = 0
    Australia = 1
    BespokeCalendar = 2
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
    NullCalendar = 22
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
    TARGET = 34
    Thailand = 35
    Turkey = 36
    Ukraine = 37
    UnitedKingdom = 38
    UnitedStates = 39
    WeekendsOnly = 40


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
    CalendarRegion.TARGET: [
        CalendarMarket.Settlement
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

available_regions = [region.name for region in CalendarRegion]

calendars_to_ql_calendars = {
    CalendarRegion.Argentina: {
        CalendarMarket.Merval: ql.Argentina(ql.Argentina.Merval),
        CalendarMarket.Settlement: ql.Argentina()
    },
    CalendarRegion.Australia: {
        CalendarMarket.Settlement: ql.Australia()
    },
    CalendarRegion.BespokeCalendar: {
        CalendarMarket.Settlement: ql.BespokeCalendar('BespokeCalendar')
    },
    CalendarRegion.Brazil: {
        CalendarMarket.Exchange: ql.Brazil(ql.Brazil.Exchange),
        CalendarMarket.Settlement: ql.Brazil(ql.Brazil.Settlement)
    },
    CalendarRegion.Canada: {
        CalendarMarket.Settlement: ql.Canada(ql.Canada.Settlement),
        CalendarMarket.TSX: ql.Canada(ql.Canada.TSX)
    },
    CalendarRegion.China: {
        CalendarMarket.IB: ql.China(ql.China.IB),
        CalendarMarket.SSE: ql.China(ql.China.SSE),
        CalendarMarket.Settlement: ql.China()
    },
    CalendarRegion.CzechRepublic: {
        CalendarMarket.PSE: ql.CzechRepublic(ql.CzechRepublic.PSE),
        CalendarMarket.Settlement: ql.CzechRepublic()
    },
    CalendarRegion.Denmark: {
        CalendarMarket.Settlement: ql.Denmark()
    },
    CalendarRegion.Finland: {
        CalendarMarket.Settlement: ql.Finland()
    },
    CalendarRegion.France: {
        CalendarMarket.Exchange: ql.France(ql.France.Exchange),
        CalendarMarket.Settlement: ql.France(ql.France.Settlement)
    },
    CalendarRegion.Germany: {
        CalendarMarket.Eurex: ql.Germany(ql.Germany.Eurex),
        CalendarMarket.FrankfurtStockExchange: ql.Germany(ql.Germany.FrankfurtStockExchange),
        CalendarMarket.Settlement: ql.Germany(ql.Germany.Settlement),
        CalendarMarket.Xetra: ql.Germany(ql.Germany.Xetra)
    },
    CalendarRegion.HongKong: {
        CalendarMarket.HKEx: ql.HongKong(ql.HongKong.HKEx),
        CalendarMarket.Settlement: ql.HongKong()
    },
    CalendarRegion.Hungary: {
        CalendarMarket.Settlement: ql.Hungary()
    },
    CalendarRegion.Iceland: {
        CalendarMarket.ICEX: ql.Iceland(ql.Iceland.ICEX),
        CalendarMarket.Settlement: ql.Iceland()
    },
    CalendarRegion.India: {
        CalendarMarket.NSE: ql.India(ql.India.NSE),
        CalendarMarket.Settlement: ql.India()
    },
    CalendarRegion.Indonesia: {
        CalendarMarket.BEJ: ql.Indonesia(ql.Indonesia.BEJ),
        CalendarMarket.JSX: ql.Indonesia(ql.Indonesia.JSX),
        CalendarMarket.Settlement: ql.Indonesia()
    },
    CalendarRegion.Israel: {
        CalendarMarket.Settlement: ql.Israel(ql.Israel.Settlement),
        CalendarMarket.TASE: ql.Israel(ql.Israel.TASE)
    },
    CalendarRegion.Italy: {
        CalendarMarket.Exchange: ql.Italy(ql.Italy.Exchange),
        CalendarMarket.Settlement: ql.Italy(ql.Italy.Settlement)
    },
    CalendarRegion.Japan: {
        CalendarMarket.Settlement: ql.Japan()
    },
    CalendarRegion.Mexico: {
        CalendarMarket.BMV: ql.Mexico(ql.Mexico.BMV),
        CalendarMarket.Settlement: ql.Mexico()
    },
    CalendarRegion.NewZealand: {
        CalendarMarket.Settlement: ql.NewZealand()
    },
    CalendarRegion.Norway: {
        CalendarMarket.Settlement: ql.Norway()
    },
    CalendarRegion.NullCalendar: {
        CalendarMarket.Settlement: ql.NullCalendar()
    },
    CalendarRegion.Poland: {
        CalendarMarket.Settlement: ql.Poland()
    },
    CalendarRegion.Romania: {
        CalendarMarket.Settlement: ql.Romania()
    },
    CalendarRegion.Russia: {
        CalendarMarket.MOEX: ql.Russia(ql.Russia.MOEX),
        CalendarMarket.Settlement: ql.Russia(ql.Russia.Settlement)
    },
    CalendarRegion.SaudiArabia: {
        CalendarMarket.Tadawul: ql.SaudiArabia(ql.SaudiArabia.Tadawul),
        CalendarMarket.Settlement: ql.SaudiArabia()
    },
    CalendarRegion.Singapore: {
        CalendarMarket.SGX: ql.Singapore(ql.Singapore.SGX),
        CalendarMarket.Settlement: ql.Singapore()
    },
    CalendarRegion.Slovakia: {
        CalendarMarket.BSSE: ql.Slovakia(ql.Slovakia.BSSE),
        CalendarMarket.Settlement: ql.Slovakia()
    },
    CalendarRegion.SouthAfrica: {
        CalendarMarket.Settlement: ql.SouthAfrica()
    },
    CalendarRegion.SouthKorea: {
        CalendarMarket.KRX: ql.SouthKorea(ql.SouthKorea.KRX),
        CalendarMarket.Settlement: ql.SouthKorea(ql.SouthKorea.Settlement)
    },
    CalendarRegion.Sweden: {
        CalendarMarket.Settlement: ql.Sweden()
    },
    CalendarRegion.Switzerland: {
        CalendarMarket.Settlement: ql.Switzerland()
    },
    CalendarRegion.Taiwan: {
        CalendarMarket.TSEC: ql.Taiwan(ql.Taiwan.TSEC),
        CalendarMarket.Settlement: ql.Taiwan()
    },
    CalendarRegion.TARGET: {
        CalendarMarket.Settlement: ql.TARGET()
    },
    CalendarRegion.Thailand: {
        CalendarMarket.Settlement: ql.Thailand()
    },
    CalendarRegion.Turkey: {
        CalendarMarket.Settlement: ql.Turkey()
    },
    CalendarRegion.Ukraine: {
        CalendarMarket.USE: ql.Ukraine(ql.Ukraine.USE),
        CalendarMarket.Settlement: ql.Ukraine()
    },
    CalendarRegion.UnitedKingdom: {
        CalendarMarket.Exchange: ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
        CalendarMarket.Metals: ql.UnitedKingdom(ql.UnitedKingdom.Metals),
        CalendarMarket.Settlement: ql.UnitedKingdom(ql.UnitedKingdom.Settlement)
    },
    CalendarRegion.UnitedStates: {
        CalendarMarket.FederalReserve: ql.UnitedStates(ql.UnitedStates.FederalReserve),
        CalendarMarket.GovernmentBond: ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        CalendarMarket.LiborImpact: ql.UnitedStates(ql.UnitedStates.LiborImpact),
        CalendarMarket.NERC: ql.UnitedStates(ql.UnitedStates.NERC),
        CalendarMarket.NYSE: ql.UnitedStates(ql.UnitedStates.NYSE),
        CalendarMarket.Settlement: ql.UnitedStates(ql.UnitedStates.Settlement)
    },
    CalendarRegion.WeekendsOnly: {
        CalendarMarket.Settlement: ql.WeekendsOnly()
    }
}
