import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.handlers.admin.base import admin_require
from server.models import User, Question, TeacherJob


class JobsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        jobs = session.query(TeacherJob)
        self.render("jobs/list.html", jobs=jobs)

