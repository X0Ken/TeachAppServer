import json
import uuid
from datetime import datetime


from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import define
from tornado.options import options
from tornado.web import Application
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from tornado_sqlalchemy import as_future
from tornado_sqlalchemy import declarative_base
from tornado_sqlalchemy import make_session_factory

from fake import fake_data
from models import DeclarativeBase
from models import User
from models import Job
from handlers.user import UserHandler
from handlers.user import UserLoginHandler
from handlers.user import UserLogoutHandler
from handlers.user import UserRegHandler
from handlers.user import TokenHandler
from handlers.job import JobHandler


define("database_url",
       default="mysql+pymysql://root:aaaaaa@localhost/my_db?charset=utf8",
       help="Main user DB")


class IndexHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        self.write('Hello Tom!')


class AsyncWebRequestHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        with self.make_session() as session:
            count = yield as_future(session.query(User).count)
        self.write('{} users so far!'.format(count))


if __name__ == '__main__':
    options.database_url = 'sqlite+pysqlite:///sqlite.db'
    session_factory = make_session_factory(options.database_url)
    fake_data(session_factory)

    Application([
        (r'/', IndexHandler),
        (r'/jobs', JobHandler),
        (r'/user', UserHandler),
        (r'/token', TokenHandler),
        (r'/user/reg', UserRegHandler),
        (r'/user/login', UserLoginHandler),
        (r'/user/logout', UserLogoutHandler),
    ], session_factory=session_factory, cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
        autoreload=True
    ).listen(8888)

    IOLoop.current().start()
