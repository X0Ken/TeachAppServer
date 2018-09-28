import datetime
import json

from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Teacher
from server.models import TeacherJob
from server.models import User
from server.utils import strutils


class TeacherJobDetailHandler(BaseAPIHandler):

    @coroutine
    def get(self, job_id):
        with self.make_session() as session:
            job = session.query(TeacherJob).filter_by(id=job_id).first()
            self.write({
                "teacherjob": job.get_info()
            })


class TeacherJobHandler(BaseAPIHandler):

    @auth_require
    def only_me(self, jobs):
        user_id = self.user.id
        jobs = jobs.filter(TeacherJob.provider == user_id)
        return jobs

    @coroutine
    def get(self):
        only_me = self.get_argument("only_me", default="false")
        only_me = strutils.bool_from_string(only_me)
        with self.make_session() as session:
            jobs = session.query(TeacherJob).filter_by(deleted=0)
            if only_me:
                jobs = self.only_me(jobs)
            self.write({
                "teacherjobs": [job.get_info() for job in jobs]
            })

    @coroutine
    @auth_require
    def put(self):
        session = self.session
        body = json.loads(self.request.body.decode('utf-8'))
        job = body.get("teacherjob")
        job = TeacherJob(provider=self.user.id, **job)
        session.add(job)
        session.flush()
        session.refresh(job)
        self.write({"teacherjob": job.get_info()})


class TeacherDetailHandler(BaseAPIHandler):

    @coroutine
    def get(self, teacher_id):
        session = self.session
        teacher = session.query(Teacher).filter_by(
            id=teacher_id).first()
        user = session.query(User).filter_by(id=teacher_id).first()
        if teacher and user:
            teacher_info = teacher.get_info()
            teacher_info['username'] = user.username
            teacher_info['success_order'] = 10
            teacher_info['good_evaluate_v'] = 0.95
            self.write({
                "teacher": teacher_info
            })
        else:
            self.set_status(404)
            self.write({"error": "Not found!"})
            return

    @coroutine
    @auth_require
    def post(self, teacher_id):
        body = json.loads(self.request.body.decode('utf-8'))
        teacher_info = body.get("teacher")
        session = self.session

        teacher = session.query(Teacher).filter_by(id=self.user.id).first()
        if teacher:
            for k, v in teacher_info.items():
                setattr(teacher, k, v)
            teacher.update_at = datetime.datetime.utcnow()
        else:
            teacher = Teacher(id=self.user.id, **teacher_info)
            session.add(teacher)
        session.flush()
        session.refresh(teacher)
        self.write({"teacher": teacher.get_info()})


class TeacherHandler(BaseAPIHandler):

    @coroutine
    def get(self):
        with self.make_session() as session:
            teachers = session.query(Teacher).filter_by(deleted=0).all()
            self.write({
                "teachers": [teacher.get_info() for teacher in teachers]
            })
