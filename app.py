import json
import uuid
from datetime import datetime

from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from tornado_sqlalchemy import (SessionMixin, as_future, declarative_base,
                                make_session_factory)

from fake import fake_data
from handlers.user import TokenHandler, UserHandler, UserDetailHandler, UserPropertyHandler
from handlers.question import QuestionHandler, QuestionDetailHandler
from handlers.teacher import TeacherDetailHandler, TeacherHandler
from handlers.teacher import TeacherJobHandler, TeacherJobDetailHandler

from models import DeclarativeBase, TeacherJob, User


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


def make_app():
    options.database_url = 'sqlite+pysqlite:///sqlite.db'
    session_factory = make_session_factory(options.database_url)
    fake_data(session_factory)

    return Application([
        (r'/', IndexHandler),
        (r'/teachers', TeacherHandler),
        (r'/teachers/([0-9a-f]{32})', TeacherDetailHandler),
        (r'/teacherjobs', TeacherJobHandler),
        (r'/teacherjobs/([0-9a-f]{32})', TeacherJobDetailHandler),
        (r'/users', UserHandler),
        (r'/users/([0-9a-f]{32})', UserDetailHandler),
        (r'/users/([0-9a-f]{32})/property', UserPropertyHandler),
        (r'/token', TokenHandler),
        (r'/questions', QuestionHandler),
        (r'/questions/([0-9a-f]{32})', QuestionDetailHandler)
    ], session_factory=session_factory, cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
        autoreload=True
    )


if __name__ == '__main__':
    make_app().listen(8888)

    IOLoop.current().start()
