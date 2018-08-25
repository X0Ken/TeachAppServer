import uuid
from datetime import datetime

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

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    # __mapper_args__ = {'always_refresh': True}

    deleted = Column(Integer, default=0)
    hidded = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v)


class User(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    pic = Column(String(255))
    role = Column(String(255))
    token_id = Column(String(255), default=default_uuid)

    def get_info(self):
        return {
            "id": self.id,
            "pic": self.pic,
            "username": self.username,
        }

    def get_token_info(self):
        info = self.get_info()
        info['token_id'] = self.token_id
        info['role'] = self.role
        return info


class UserProperty(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    property = Column(String(255))
    value = Column(String(255))


class TeacherJob(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    method = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(Integer)
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))
    provider = Column(Integer)

    def get_info(self):
        return {
            "id": self.id,
            "method": self.method,
            "gender": self.gender,
            "school": self.school,
            "highest_education": self.highest_education,
            "pay": self.pay,
            "region": self.region,
            "subject": self.subject,
            "time": self.time,
            "provider": self.provider,
            "create_at": self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Teacher(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
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
            "id": self.id,
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

    id = Column(Integer, primary_key=True)
    content = Column(String(255))
    keywords = Column(String(255))
    pay = Column(Integer)
    asker = Column(Integer)
    fixed = Column(Integer, default=0)

    def get_info(self):
        return {
            'id': self.id,
            "content": self.content,
            "keywords": self.keywords,
            "pay": self.pay,
            "asker": self.asker,
            "fixed": self.fixed
        }


class Order(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    # payer -> payee
    payer = Column(Integer)
    payee = Column(Integer)
    amount = Column(Integer)  # real =  pay / 100


class Msg(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    sender = Column(Integer)
    receiver = Column(Integer)
    content = Column(String(255))
    unread = Column(Integer, default=1)
    
    def get_info(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content,
            'unread': self.unread
        }
