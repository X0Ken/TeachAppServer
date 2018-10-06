import os
from functools import wraps

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from server.models import User


class BaseAdminHandler(SessionMixin, RequestHandler):
    user = None
    loader = None

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), "templates")

    def get_current_user(self):
        token_id = self.get_cookie('token-id')
        if not token_id:
            return None
        user = self.session.query(User).filter_by(token_id=token_id).first()
        if not user or user.role != 'admin':
            return None
        return user


def admin_require(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        user = self.current_user
        if not user or user.role != 'admin':
            self.redirect("/admin/login")
            return
        return f(self, *args, **kwargs)
    return wrapper
