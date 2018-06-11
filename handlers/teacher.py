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

from models import DeclarativeBase
from models import User
from models import Job
from models import Teacher
from handlers import BaseHandler


class JobDetailHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self, job_id):
        with self.make_session() as session:
            job = session.query(Job).filter_by(uuid=job_id).first()
            self.write({
                "job": job.get_info()
            })


class JobHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self):
        with self.make_session() as session:
            jobs = session.query(Job).filter_by(deleted=0).all()
            self.write({
                "jobs": [job.get_info() for job in jobs]
            })

    @coroutine
    def post(self):
        job_uuid = uuid.uuid4().hex
        body = json.loads(self.request.body)
        job = body.get("job")
        with self.make_session() as session:
            job = Job(uuid=job_uuid, **job)
            session.add(job)
        with self.make_session() as session:
            job = session.query(Job).filter_by(uuid=job_uuid).first()
            self.write({"job": job.get_info()})


class TeacherDetailHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self, teacher_id):
        with self.make_session() as session:
            teacher = session.query(Teacher).filter_by(
                uuid=teacher_id).first()
            self.write({
                "teacher": teacher.get_info()
            })


class TeacherHandler(BaseHandler, SessionMixin):

    @coroutine
    def get(self):
        with self.make_session() as session:
            teachers = session.query(Teacher).filter_by(deleted=0).all()
            self.write({
                "teachers": [teacher.get_info() for teacher in teachers]
            })

    @coroutine
    def post(self):
        token_id = self.request.headers.get('token-id')
        print("Headers: {}".format(self.request.headers))
        print("Token-Id: {}".format(token_id))
        if not token_id:
            self.set_status(401)
            self.write({"error": "Not auth!"})
            return

        teacher_id = None
        body = json.loads(self.request.body)
        teacher_info = body.get("teacher")
        with self.make_session() as session:
            user = session.query(User).filter_by(token_id=token_id).first()
            if user:
                teacher_id = user.uuid
            else:
                self.set_status(401)
                self.write({"error": "Not auth!"})
                return
            teacher = session.query(Teacher).filter_by(uuid=teacher_id).first()
            if teacher:
                for k, v in teacher_info.items():
                    setattr(teacher, k, v)
            else:
                teacher = Teacher(uuid=teacher_id, **teacher_info)
                session.add(teacher)
            session.commit()
            teacher = session.query(Teacher).filter_by(
                uuid=teacher_id).first()
            self.write({"teacher": teacher.get_info()})