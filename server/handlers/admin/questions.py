import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.handlers.admin.base import admin_require
from server.models import User, Question


class QuestionsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        questions = session.query(Question)
        self.render("questions/list.html", questions=questions)

