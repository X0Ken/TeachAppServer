import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.handlers.admin.base import admin_require
from server.models import User, Question, TeacherJob, Teacher


class TeachersHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        teachers = session.query(Teacher)
        self.render("teachers/list.html", teachers=teachers, info=None)

