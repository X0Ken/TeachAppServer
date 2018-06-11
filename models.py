from datetime import datetime
import uuid

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from tornado_sqlalchemy import declarative_base


DeclarativeBase = declarative_base()

AVALIBLE_ROLE = ['user', 'admin']
AVALIBLE_METHOD = ['remote', 'home']
AVALIBLE_GENDER = ['male ', 'female']
AVALIBLE_EDUCATION = ['Undergraduate', 'master', 'PhD']


def default_uuid():
    return uuid.uuid4().hex


class ObjectMixin(object):

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    # __mapper_args__ = {'always_refresh': True}

    uuid = Column(String(32), primary_key=True, default=default_uuid)
    deleted = Column(Integer, default=0)
    hidded = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)


class User(DeclarativeBase, ObjectMixin):

    username = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(255))
    token_id = Column(String(255), default=default_uuid)

    def get_info(self):
        return {
            "id": self.uuid,
            "username": self.username,
        }

    def get_token_info(self):
        return {
            "token_id": self.token_id,
            "username": self.username,
            "id": self.uuid,
            "role": self.role,
        }


class UserProperty(DeclarativeBase, ObjectMixin):

    user_id = Column(String(255))
    property = Column(String(255))
    value = Column(String(255))


class Job(DeclarativeBase, ObjectMixin):

    method = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(String(255))
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))

    def get_info(self):
        return {
            "id": self.uuid,
            "method": self.method,
            "gender": self.gender,
            "school": self.school,
            "highest_education": self.highest_education,
            "pay": self.pay,
            "region": self.region,
            "subject": self.subject,
            "time": self.time,
            "create_at": self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Teacher(DeclarativeBase, ObjectMixin):

    method = Column(String(255))
    idcard = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    school_subject = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(String(255))
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))
    self_evaluate = Column(String(255))

    def get_info(self):
        return {
            "user_id": self.uuid,
            "idcard": self.idcard,
            "method": self.method,
            "gender": self.gender,
            "school": self.school,
            "school_subject": self.school_subject,
            "highest_education": self.highest_education,
            "pay": self.pay,
            "region": self.region,
            "subject": self.subject,
            "time": self.time,
            "self_evaluate": self.self_evaluate,
            "create_at": self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Question(DeclarativeBase, ObjectMixin):

    context = Column(String(255))
    keywords = Column(String(255))

    def get_info(self):
        return {
            'id': self.uuid,
            "context": self.context,
            "keywords": self.keywords
        }


class Order(DeclarativeBase, ObjectMixin):

    user1 = Column(String(255))
    user2 = Column(String(255))
    pay = Column(String(255))
