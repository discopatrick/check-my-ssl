import datetime as dt
import socket, ssl


def ssl_expiry_date(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()

    return dt.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def days_until(a_datetime):
    return (a_datetime - dt.datetime.utcnow()).days


def days_until_ssl_expiry(hostname):
    expiry = ssl_expiry_date(hostname)

    return days_until(expiry)
