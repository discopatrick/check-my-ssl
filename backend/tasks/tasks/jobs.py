import logging
import os
from socket import gaierror

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
import sentry_sdk

from persistence.database import db_session
from persistence.models import DomainName, get_or_create, SSLCheck
from ssl_checker import days_until_ssl_expiry
from tasks.middleware import SentryMiddleware

rabbitmq_broker = RabbitmqBroker(host='broker')
dramatiq.set_broker(rabbitmq_broker)
sentry_sdk.init(dsn=os.environ['SENTRY_DSN'])
rabbitmq_broker.add_middleware(SentryMiddleware(sentry_sdk.capture_exception))
LOG = logging.getLogger(__name__)


@dramatiq.actor
def days_until_ssl_expiry_job(hostname):
    LOG.info('days_until_ssl_expiry_job')
    try:
        days_left = days_until_ssl_expiry(hostname)
    except gaierror as e:
        logging.error(f'Error processing job: {str(e)}')
        return

    # funky = 1 / 0  # TODO: ensure this gets to Sentry (import Sentry config at the top of this file?)

    LOG.info(f'{hostname} SSL has {days_left} days until expiry')
    domain_name = get_or_create(session=db_session, model=DomainName, domain_name=hostname)
    db_session.add(SSLCheck(domain_name=domain_name, days_until_ssl_expiry=days_left))
    db_session.commit()


@dramatiq.actor
def check_ssl_for_all_domain_names():
    LOG.info('check_ssl_for_all_domain_names')
    all_domain_names = db_session.query(DomainName).all()
    for dn in all_domain_names:
        days_until_ssl_expiry_job.send(dn.domain_name)


@dramatiq.actor(max_retries=0)
def invoke_exception_task():
    LOG.info('Running the invoke_exception_task')
    funky = 1 / 0
