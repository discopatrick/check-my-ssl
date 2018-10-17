from socket import gaierror

import dramatiq

from ssl_checker.ssl_checker import days_until_ssl_expiry


@dramatiq.actor
def days_until_ssl_expiry_job(hostname):
    try:
        days_left = days_until_ssl_expiry(hostname)
    except gaierror as e:
        print(f'Error processing job: {str(e)}')
    else:
        print(f'{days_left} days left')
