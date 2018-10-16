import datetime as dt

from ssl_checker.ssl_checker import days_between


def test_days_between():
    date_one = dt.datetime(year=2000, month=1, day=1, hour=12)
    date_two = dt.datetime(year=2000, month=1, day=3, hour=13)

    result = days_between(date_one, date_two)

    assert result == 2
