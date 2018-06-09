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


class QuestionHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self):
        self.finish()

    @coroutine
    def post(self):
        self.finish()
