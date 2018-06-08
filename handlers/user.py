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


class UserRegHandler(BaseHandler, SessionMixin):
    @coroutine
    def get(self):
        self.write("""
<form method="post">
 First name:<br>
<input type="text" name="username">
<br>
 Password:<br>
<input type="password" name="password">
<br><br>
<input type="submit" value="Submit">
</form> 
            """)

    @coroutine
    def post(self):
        username = self.get_argument('username', default="", strip=True)
        password = self.get_argument('password', default="", strip=True)

        user = User(username=username, password=password)

        with self.make_session() as session:
            session.add(user)
        self.redirect('/user/login')


class UserLoginHandler(BaseHandler, SessionMixin):
    @coroutine
    def get(self):
        err = self.get_argument('err', default='none')
        if err == "user":
            msg = "username not found"
        elif err == "pass":
            msg = "password error"
        else:
            msg = ""

        self.write("""
{}
<form method="post">
 User name:<br>
<input type="text" name="username">
<br>
 Password:<br>
<input type="password" name="password">
<br><br>
<input type="submit" value="Submit">
</form> 
            """ % msg)

    @coroutine
    def post(self):
        username = self.get_argument('username', default="", strip=True)
        password = self.get_argument('password', default="", strip=True)

        with self.make_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                if password == user.password:
                    self.set_cookie("username", username)
                    self.redirect('/user')
                else:
                    self.redirect('/user/login?err=pass')
            else:
                self.redirect('/user/login?err=user')


class UserLogoutHandler(BaseHandler, SessionMixin):
    @coroutine
    def get(self):
        self.clear_cookie("username")
        self.redirect('/user/login')


class UserHandler(BaseHandler, SessionMixin):
    @coroutine
    def get(self):
        username = self.get_cookie("username")
        if username:
            login = '<a href="/user/logout">login out</a>'
        else:
            login = '<a href="/user/login">login</a>'

        self.write("""
            Hello {} !<br/>
            {}
            """.format(username, login))


class TokenHandler(BaseHandler, SessionMixin):
    def get_token(self, user):
        return {
            "token": {
                "id": user.token_id,
                "username": user.username,
                "role": user.role,
            }
        }

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
            self.write(self.get_token(user))

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

            self.write(self.get_token(user))

    @coroutine
    def post(self):
        body = json.loads(self.request.body)
        auth = body.get("auth")
        auth_type = auth.get('type')
        if auth_type == "password":
            self.auth_password(auth)
        elif auth_type == "token":
            self.auth_token(auth)
