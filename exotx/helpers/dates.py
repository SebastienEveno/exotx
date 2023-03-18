from datetime import datetime
from typing import Union

import QuantLib as ql


def convert_maturity_to_ql_date(maturity: Union[str, datetime, ql.Date], string_format: str = '%Y-%m-%d') -> ql.Date:
    if isinstance(maturity, ql.Date):
        return maturity
    elif isinstance(maturity, datetime):
        return ql.Date.from_date(maturity)
    elif isinstance(maturity, str):
        datetime_maturity = datetime.strptime(maturity, string_format)
        return convert_maturity_to_ql_date(datetime_maturity)
    else:
        raise TypeError(f"Invalid maturity type: {type(maturity)}")
