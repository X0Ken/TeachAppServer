import datetime
import json

from tornado.gen import coroutine

from server.handlers.api import BaseAPIHandler
from server.handlers.api import auth_require
from server.models import Question


class QuestionDetailHandler(BaseAPIHandler):
    @coroutine
    def get(self, question_id):
        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        if not question:
            self.set_status(404)
            self.write({"error": "Question not found!"})
            return
        self.write({
            "question": question.get_info()
        })

    @coroutine
    @auth_require
    def delete(self, question_id):
        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        if not question:
            self.set_status(404)
            self.write({"error": "Question not found!"})
            return
        question.deleted = 1
        question.delete_at = datetime.datetime.utcnow()
        session.flush()

    @coroutine
    @auth_require
    def post(self, question_id):
        body = json.loads(self.request.body.decode('utf-8'))
        question = body.get("question")

        keywords = question['keywords']
        content = question['content']
        pay = question['pay']
        fixed = question['fixed']

        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        question.update_at = datetime.datetime.utcnow()
        question.keywords = keywords
        question.content = content
        question.pay = pay
        question.fixed = fixed
        session.flush()
        session.refresh(question)
        self.write({"question": question.get_info()})


class QuestionHandler(BaseAPIHandler):

    @coroutine
    def get(self):
        session = self.session
        questions = session.query(Question).all()
        self.write({
            "questions": [
                q.get_info() for q in questions
            ]
        })

    @coroutine
    @auth_require
    def put(self):
        body = json.loads(self.request.body.decode('utf-8'))
        question = body.get("question")

        keywords = question['keywords']
        content = question['content']
        pay = question['pay']

        question = Question(
            keywords=keywords,
            content=content,
            pay=pay,
            asker=self.user.id
        )

        session = self.session
        session.add(question)
        session.flush()
        session.refresh(question)
        self.write({"question": question.get_info()})
