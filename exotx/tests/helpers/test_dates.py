import QuantLib as ql
import pytest

from exotx.helpers.dates import convert_maturity_to_ql_date


@pytest.mark.parametrize("maturity, expected_output, date_format", [
    ("2022-12-31", ql.Date(31, 12, 2022), "%Y-%m-%d"),
    ("12/31/2022", ql.Date(31, 12, 2022), "%m/%d/%Y"),
    ("2022/12/31", ql.Date(31, 12, 2022), "%Y/%m/%d"),
    ("31-12-2022", ql.Date(31, 12, 2022), "%d-%m-%Y"),
    ("31.12.2022", ql.Date(31, 12, 2022), "%d.%m.%Y")
])
def test_convert_maturity_to_ql_date(maturity, expected_output, date_format):
    assert convert_maturity_to_ql_date(maturity, date_format) == expected_output


def test_convert_maturity_to_ql_date_invalid_date():
    with pytest.raises(ValueError, match="unconverted data remains"):
        convert_maturity_to_ql_date("2022-01-32")


def test_convert_maturity_to_ql_date_invalid_date_format():
    with pytest.raises(ValueError) as e:
        convert_maturity_to_ql_date("2022/01/01")
    assert "time data '2022/01/01' does not match format '%Y-%m-%d'" in str(e.value)
