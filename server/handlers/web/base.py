import os
from functools import wraps

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from server.models import User


class BaseHandler(SessionMixin, RequestHandler):
    user = None
    loader = None

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), "templates")
