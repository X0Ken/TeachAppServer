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


class JobHandler(BaseHandler, SessionMixin):
    def get_job(self, job):
        return {
            "uuid": job.uuid,
            "method": job.method,
            "gender": job.gender,
            "school": job.school,
            "highest_education": job.highest_education,
            "pay": job.pay,
            "region": job.region,
            "subject": job.subject,
            "time": job.time,
            "create_at": job.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @coroutine
    def get(self):
        with self.make_session() as session:
            jobs = session.query(Job).filter_by(deleted=0).all()
            jobs = (self.get_job(job) for job in jobs)
            self.write({
                "jobs": [job for job in jobs]
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
            self.write({"Job": self.get_job(job)})
