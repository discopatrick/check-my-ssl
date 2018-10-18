from socket import gaierror

import dramatiq

from backend.database import db_session
from backend.models import DomainName, get_or_create, SSLCheck
from ssl_checker.ssl_checker import days_until_ssl_expiry


@dramatiq.actor
def days_until_ssl_expiry_job(hostname):
    try:
        days_left = days_until_ssl_expiry(hostname)
    except gaierror as e:
        print(f'Error processing job: {str(e)}')
        return

    print(f'{hostname} SSL has {days_left} days until expiry')
    domain_name = get_or_create(session=db_session, model=DomainName, domain_name=hostname)
    db_session.add(SSLCheck(domain_name=domain_name, days_until_ssl_expiry=days_left))
    db_session.commit()
