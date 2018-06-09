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

from fake import fake_data
from models import DeclarativeBase
from models import User
from models import Job
from handlers import BaseHandler


class UserInfoHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self, user_id):
        with self.make_session() as session:
            user = session.query(User).filter_by(uuid=user_id).first()
            self.write(user.get_user_info())


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
            self.write(user.get_token_info())


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
            self.write(user.get_token_info())

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

            self.write(user.get_token_info())

    @coroutine
    def post(self):
        body = json.loads(self.request.body)
        auth = body.get("auth")
        auth_type = auth.get('type')
        if auth_type == "password":
            self.auth_password(auth)
        elif auth_type == "token":
            self.auth_token(auth)
