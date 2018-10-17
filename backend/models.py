from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DomainName(Base):
    __tablename__ = 'domain_names'
    id = Column(Integer, primary_key=True)
    domain_name = Column(String(255))

    def __init__(self, domain_name):
        self.domain_name = domain_name

    def __str__(self):
        return f'<DomainName "{self.domain_name}">'

    def __repr__(self):
        return f'<DomainName "{self.domain_name}">'
