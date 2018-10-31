import datetime as dt

from ssl_checker import days_until


def test_days_until():
    future_time = dt.datetime.utcnow() + dt.timedelta(days=2, hours=1)

    result = days_until(future_time)

    assert result == 2
