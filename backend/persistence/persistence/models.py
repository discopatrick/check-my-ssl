import datetime as dt
import logging

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

LOG = logging.getLogger(__name__)


class SSLCheck(Base):
    __tablename__ = 'ssl_checks'

    id = Column(Integer, primary_key=True)
    domain_name_id = Column(Integer, ForeignKey('domain_names.id'))
    checked_at = Column(DateTime, default=dt.datetime.utcnow)
    days_until_ssl_expiry = Column(Integer, nullable=True)
    domain_name = relationship('DomainName', back_populates='ssl_checks')

    def __init__(self, domain_name, days_until_ssl_expiry):
        LOG.info('SSLCheck __init__')
        self.domain_name = domain_name
        self.days_until_ssl_expiry = days_until_ssl_expiry

    def __str__(self):
        return f'<SSLCheck domain_name="{self.domain_name}", checked_at="{self.checked_at}">'

    def __repr__(self):
        return self.__str__()


class DomainName(Base):
    __tablename__ = 'domain_names'

    id = Column(Integer, primary_key=True)
    domain_name = Column(String(255), unique=True)
    ssl_checks = relationship('SSLCheck', back_populates='domain_name')

    def __init__(self, domain_name):
        LOG.info('DomainName __init__')
        self.domain_name = domain_name

    def __str__(self):
        return f'<DomainName "{self.domain_name}">'

    def __repr__(self):
        return self.__str__()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
