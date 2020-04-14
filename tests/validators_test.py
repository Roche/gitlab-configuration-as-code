import pytest

from gcasc.utils import validators


@pytest.mark.parametrize("date", ["2001-01-01", "2050-12-31"])
def test_date_success_validation(date):
    # expect
    assert validators.validate_date(date)


@pytest.mark.parametrize("date", ["2001-jan-01", "31-12-2050", "2050 10 12", ""])
def test_date_failure_validation(date):
    # expect
    assert not validators.validate_date(date)
