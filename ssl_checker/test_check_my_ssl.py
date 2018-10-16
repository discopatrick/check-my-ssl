import datetime as dt

import pytest

from check_my_ssl import (
    days_between,
    days_until,
)

def test_days_between():
    date_one = dt.datetime(year=2000, month=1, day=1, hour=12)
    date_two = dt.datetime(year=2000, month=1, day=3, hour=13)

    result = days_between(date_one, date_two)

    assert result == 2


def test_days_until():
    future_time = dt.datetime.utcnow() + dt.timedelta(days=2, hours=1)

    result = days_until(future_time)

    assert result == 2
