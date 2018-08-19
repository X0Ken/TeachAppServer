from functools import wraps

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from server.models import User


class BaseAPIHandler(RequestHandler, SessionMixin):
    user = None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Content-Type, token-id")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()


def auth_require(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        s = args[0]
        token_id = s.request.headers.get('token-id')
        if not token_id:
            s.set_status(401)
            s.write({"error": "Not auth!"})
            return
        user = s.session.query(User).filter_by(token_id=token_id).first()
        if not user:
            s.set_status(401)
            s.write({"error": "Auth invalid!"})
            return
        s.user = user
        return f(*args, **kwargs)
    return wrapper


def admin_require(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        s = args[0]
        token_id = s.request.headers.get('token-id')
        if not token_id:
            s.set_status(401)
            s.write({"error": "Not auth!"})
            return
        user = s.session.query(User).filter_by(token_id=token_id).first()
        if not user or user.role != 'admin':
            s.set_status(401)
            s.write({"error": "Auth invalid!"})
            return
        s.user = user
        return f(*args, **kwargs)
    return wrapper
