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
