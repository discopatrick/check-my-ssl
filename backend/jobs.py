import logging
from socket import gaierror

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from backend.database import db_session
from backend.models import DomainName, get_or_create, SSLCheck
from ssl_checker.ssl_checker import days_until_ssl_expiry

rabbitmq_broker = RabbitmqBroker(host='broker')
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def days_until_ssl_expiry_job(hostname):
    try:
        days_left = days_until_ssl_expiry(hostname)
    except gaierror as e:
        logging.error(f'Error processing job: {str(e)}')
        return

    funky = 1 / 0  # TODO: ensure this gets to Sentry (import Sentry config at the top of this file?)

    logging.info(f'{hostname} SSL has {days_left} days until expiry')
    domain_name = get_or_create(session=db_session, model=DomainName, domain_name=hostname)
    db_session.add(SSLCheck(domain_name=domain_name, days_until_ssl_expiry=days_left))
    db_session.commit()


@dramatiq.actor
def check_ssl_for_all_domain_names():
    all_domain_names = db_session.query(DomainName).all()
    for dn in all_domain_names:
        days_until_ssl_expiry_job.send(dn.domain_name)
