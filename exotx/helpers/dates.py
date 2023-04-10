from datetime import datetime
from typing import Union

import QuantLib as ql


def convert_maturity_to_ql_date(maturity: Union[str, datetime, ql.Date], string_format: str = '%Y-%m-%d') -> ql.Date:
    """
    Converts a maturity date in various formats to a QuantLib Date object.

    This function accepts input dates as strings, Python datetime objects, or QuantLib Date objects and
    returns the corresponding QuantLib Date object.

    :param maturity: The maturity date to be converted, which can be a string, datetime, or QuantLib Date object.
    :type maturity: Union[str, datetime, ql.Date]
    :param string_format: The date format for string input, defaults to '%Y-%m-%d'.
    :type string_format: str, optional
    :return: The converted maturity date as a QuantLib Date object.
    :rtype: ql.Date
    :raises TypeError: If the input maturity type is not valid.
    """
    if isinstance(maturity, ql.Date):
        return maturity
    elif isinstance(maturity, datetime):
        return ql.Date.from_date(maturity)
    elif isinstance(maturity, str):
        datetime_maturity = datetime.strptime(maturity, string_format)
        return convert_maturity_to_ql_date(datetime_maturity)
    else:
        raise TypeError(f"Invalid maturity type: {type(maturity)}")
