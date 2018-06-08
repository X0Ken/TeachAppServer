from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from tornado_sqlalchemy import declarative_base


DeclarativeBase = declarative_base()

AVALIBLE_ROLE = ['teach', 'student', 'administrator']
AVALIBLE_METHOD = ['remote', 'home']
AVALIBLE_GENDER = ['male ', 'female']
AVALIBLE_EDUCATION = ['Undergraduate', 'master', 'PhD']


class User(DeclarativeBase):
    __tablename__ = 'users'

    uuid = Column(String(32), primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(255))
    token_id = Column(String(255))


class Job(DeclarativeBase):
    __tablename__ = 'jobs'

    uuid = Column(String(32), primary_key=True)
    # 授课方式
    method = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(String(255))
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))

    deleted = Column(BigInteger, default=0)
    hidded = Column(BigInteger, default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)
