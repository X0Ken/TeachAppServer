import json
import uuid

from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import User
from server.models import UserProperty


class UserDetailHandler(BaseAPIHandler):

    @coroutine
    def get(self, user_id):
        session = self.session
        user = session.query(User).filter_by(id=user_id).first()
        self.write({"user": user.get_info()})


class UserHandler(BaseAPIHandler):

    @coroutine
    def PUT(self):
        session = self.session
        token_id = uuid.uuid4().hex
        body = json.loads(self.request.body.decode('utf-8'))
        user = body.get("register")

        username = user['username']
        password = user['password']

        user = User(username=username,
                    password=password, role='user', token_id=token_id)

        session.add(user)
        session.flush()
        session.refresh(user)
        self.write({"token": user.get_token_info()})


class UserPropertyHandler(BaseAPIHandler):
    @coroutine
    @auth_require
    def get(self, user_id):
        self.write({"token": 'dd'})

    @coroutine
    @auth_require
    def post(self, user_id):
        body = json.loads(self.request.body.decode('utf-8'))
        pros_new = body.get("property")
        session = self.session
        for k, v in pros_new.items():
            pro = session.query(UserProperty).filter_by(
                user_id=user_id, property=k).first()
            if pro:
                pro.value = v
            else:
                pro = UserProperty(property=k, value=v)
                session.add(pro)
        session.flush()
        pros = session.query(UserProperty).filter_by(
            user_id=user_id).all()
        r = {}
        for pro in pros:
            r[pro.property] = pro.value
        self.write({"property": r})

    @coroutine
    @auth_require
    def put(self, user_id):
        self.write({"token": 'dd'})

    @coroutine
    @auth_require
    def delete(self, user_id):
        self.write({"token": 'dd'})


class TokenHandler(BaseAPIHandler):

    def auth_password(self, auth):
        username = auth.get('username')
        password = auth.get('password')
        user_id = None

        session = self.session
        user = session.query(User).filter_by(username=username).first()
        if user and password == user.password:
            user.token_id = uuid.uuid4().hex
            user_id = user.id

        if not user_id:
            self.set_status(401)
            self.write({
                "error": "User or password error!"
            })
            return

        session.flush()
        session.refresh(user)
        self.write({"token": user.get_token_info()})

    def auth_token(self, auth):
        token_id = auth.get('token_id')

        session = self.session
        user = session.query(User).filter_by(token_id=token_id).first()

        if not user:
            self.set_status(401)
            self.write({
                "error": "Auth error!"
            })
            return

        self.write({"token": user.get_token_info()})

    @coroutine
    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        auth = body.get("auth")
        auth_type = auth.get('type')
        if auth_type == "password":
            self.auth_password(auth)
        elif auth_type == "token":
            self.auth_token(auth)
