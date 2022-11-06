import QuantLib as ql

# based on https://quantlib-python-docs.readthedocs.io/en/latest/dates.html#calendar
calendars = {
    'Argentina': {
        'Merval': ql.Argentina(ql.Argentina.Merval),
        'default': ql.Argentina()
    },
    'Australia': {
        'default': ql.Australia()
    },
    'BespokeCalendar': {
        'default': ql.BespokeCalendar('BespokeCalendar')
    },
    'Brazil': {
        'Exchange': ql.Brazil(ql.Brazil.Exchange),
        'Settlement': ql.Brazil(ql.Brazil.Settlement),
        'default': ql.Brazil()
    },
    'Canada': {
        'Settlement': ql.Canada(ql.Canada.Settlement),
        'TSX': ql.Canada(ql.Canada.TSX),
        'default': ql.Canada()
    },
    'China': {
        'IB': ql.China(ql.China.IB),
        'SSE': ql.China(ql.China.SSE),
        'default': ql.China()
    },
    'CzechRepublic': {
        'PSE': ql.CzechRepublic(ql.CzechRepublic.PSE),
        'default': ql.CzechRepublic()
    },
    'Denmark': {
        'default': ql.Denmark()
    },
    'Finland': {
        'default': ql.Finland()
    },
    'France': {
        'Exchange': ql.France(ql.France.Exchange),
        'Settlement': ql.France(ql.France.Settlement),
        'default': ql.France()
    },
    'Germany': {
        'Eurex': ql.Germany(ql.Germany.Eurex),
        'FrankfurtStockExchange': ql.Germany(ql.Germany.FrankfurtStockExchange),
        'Settlement': ql.Germany(ql.Germany.Settlement),
        'Xetra': ql.Germany(ql.Germany.Xetra),
        'default': ql.Germany()
    },
    'HongKong': {
        'HKEx': ql.HongKong(ql.HongKong.HKEx),
        'default': ql.HongKong()
    },
    'Hungary': {
        'default': ql.Hungary()
    },
    'Iceland': {
        'ICEX': ql.Iceland(ql.Iceland.ICEX),
        'default': ql.Iceland()
    },
    'India': {
        'NSE': ql.India(ql.India.NSE),
        'default': ql.India()
    },
    'Indonesia': {
        'BEJ': ql.Indonesia(ql.Indonesia.BEJ),
        'JSX': ql.Indonesia(ql.Indonesia.JSX),
        'default': ql.Indonesia()
    },
    'Israel': {
        'Settlement': ql.Israel(ql.Israel.Settlement),
        'TASE': ql.Israel(ql.Israel.TASE),
        'default': ql.Israel()
    },
    'Italy': {
        'Exchange': ql.Italy(ql.Italy.Exchange),
        'Settlement': ql.Italy(ql.Italy.Settlement),
        'default': ql.Italy()
    },
    'Japan': {
        'default': ql.Japan()
    },
    'Mexico': {
        'BMV': ql.Mexico(ql.Mexico.BMV),
        'default': ql.Mexico()
    },
    'NewZealand': {
        'default': ql.NewZealand()
    },
    'Norway': {
        'default': ql.Norway()
    },
    'NullCalendar': {
        'default': ql.NullCalendar()
    },
    'Poland': {
        'default': ql.Poland()
    },
    'Romania': {
        'default': ql.Romania()
    },
    'Russia': {
        'MOEX': ql.Russia(ql.Russia.MOEX),
        'Settlement': ql.Russia(ql.Russia.Settlement),
        'default': ql.Russia()
    },
    'SaudiArabia': {
        'Tadawul': ql.SaudiArabia(ql.SaudiArabia.Tadawul),
        'default': ql.SaudiArabia()
    },
    'Singapore': {
        'SGX': ql.Singapore(ql.Singapore.SGX),
        'default': ql.Singapore()
    },
    'Slovakia': {
        'BSSE': ql.Slovakia(ql.Slovakia.BSSE),
        'default': ql.Slovakia()
    },
    'SouthAfrica': {
        'default': ql.SouthAfrica()
    },
    'SouthKorea': {
        'KRX': ql.SouthKorea(ql.SouthKorea.KRX),
        'Settlement': ql.SouthKorea(ql.SouthKorea.Settlement),
        'default': ql.SouthKorea()
    },
    'Sweden': {
        'default': ql.Sweden()
    },
    'Switzerland': {
        'default': ql.Switzerland()
    },
    'Taiwan': {
        'TSEC': ql.Taiwan(ql.Taiwan.TSEC),
        'default': ql.Taiwan()
    },
    'TARGET': {
        'default': ql.TARGET()
    },
    'Thailand': {
        'default': ql.Thailand()
    },
    'Turkey': {
        'default': ql.Turkey()
    },
    'Ukraine': {
        'USE': ql.Ukraine(ql.Ukraine.USE),
        'default': ql.Ukraine()
    },
    'UnitedKingdom': {
        'Exchange': ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
        'Metals': ql.UnitedKingdom(ql.UnitedKingdom.Metals),
        'Settlement': ql.UnitedKingdom(ql.UnitedKingdom.Settlement),
        'default': ql.UnitedKingdom()
    },
    'UnitedStates': {
        'FederalReserve': ql.UnitedStates(ql.UnitedStates.FederalReserve),
        'GovernmentBond': ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        'LiborImpact': ql.UnitedStates(ql.UnitedStates.LiborImpact),
        'NERC': ql.UnitedStates(ql.UnitedStates.NERC),
        'NYSE': ql.UnitedStates(ql.UnitedStates.NYSE),
        'Settlement': ql.UnitedStates(ql.UnitedStates.Settlement),
        'default': ql.UnitedStates()
    },
    'WeekendsOnly': {
        'default': ql.WeekendsOnly()
    }
}
