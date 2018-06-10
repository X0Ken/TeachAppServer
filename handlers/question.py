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
from models import Question
from handlers import BaseHandler


class QuestionHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self):
        with self.make_session() as session:
            questions = session.query(Question).all()
            self.write({
                "questions": [
                    q.get_info() for q in questions
                ]
            })

    @coroutine
    def post(self):
        question_id = uuid.uuid4().hex
        body = json.loads(self.request.body)
        question = body.get("question")

        keywords = question['username']
        context = question['context']

        question = Question(
            uuid=question_id, keywords=keywords, context=context)

        with self.make_session() as session:
            session.add(question)
        with self.make_session() as session:
            question = session.query(Question).filter_by(
                uuid=question_id).first()
            self.write({"question": question.get_info()})
