import json
import uuid
from datetime import datetime


from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import define
from tornado.options import options
from tornado.web import Application
from tornado_sqlalchemy import SessionMixin
from tornado_sqlalchemy import as_future
from tornado_sqlalchemy import declarative_base
from tornado_sqlalchemy import make_session_factory

from models import User, UserProperty
from handlers import BaseHandler


class UserDetailHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self, user_id):
        with self.make_session() as session:
            user = session.query(User).filter_by(uuid=user_id).first()
            self.write({"user": user.get_info()})


class UserHandler(BaseHandler, SessionMixin):

    @coroutine
    def post(self):
        user_id = uuid.uuid4().hex
        token_id = uuid.uuid4().hex
        body = json.loads(self.request.body)
        user = body.get("register")

        username = user['username']
        password = user['password']

        user = User(uuid=user_id, username=username,
                    password=password, role='user', token_id=token_id)

        with self.make_session() as session:
            session.add(user)
        with self.make_session() as session:
            user = session.query(User).filter_by(uuid=user_id).first()
            self.write({"token": user.get_token_info()})


class UserPropertyHandler(BaseHandler, SessionMixin):
    @coroutine
    def get(self, user_id):
        self.write({"token": 'dd'})

    @coroutine
    def post(self, user_id):
        body = json.loads(self.request.body)
        pros_new = body.get("property")
        with self.make_session() as session:
            for k, v in pros_new.items():
                pro = session.query(UserProperty).filter_by(
                    user_id=user_id, property=k).first()
                if pro:
                    pro.value = v
                else:
                    pro = UserProperty(property=k, value=v)
                    session.add(pro)
            session.commit()
            pros = session.query(UserProperty).filter_by(
                user_id=user_id).all()
            r = {}
            for pro in pros:
                r[pro.property] = pro.value
            self.write({"property": r})

    @coroutine
    def put(self, user_id):
        self.write({"token": 'dd'})

    @coroutine
    def delete(self, user_id):
        self.write({"token": 'dd'})


class TokenHandler(BaseHandler, SessionMixin):

    def auth_password(self, auth):
        username = auth.get('username')
        password = auth.get('password')
        user_id = None

        with self.make_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and password == user.password:
                user.token_id = uuid.uuid4().hex
                user_id = user.uuid

        print("user {}".format(user_id))
        if not user_id:
            self.set_status(401)
            self.write({
                "error": "User not found!"
            })
            return

        with self.make_session() as session:
            user = session.query(User).filter_by(uuid=user_id).first()
            self.write({"token": user.get_token_info()})

    def auth_token(self, auth):
        token_id = auth.get('token_id')

        with self.make_session() as session:
            user = session.query(User).filter_by(token_id=token_id).first()

            if not user:
                self.set_status(401)
                self.write({
                    "error": "User not found!"
                })
                return

            self.write({"token": user.get_token_info()})

    @coroutine
    def post(self):
        body = json.loads(self.request.body)
        auth = body.get("auth")
        auth_type = auth.get('type')
        if auth_type == "password":
            self.auth_password(auth)
        elif auth_type == "token":
            self.auth_token(auth)
