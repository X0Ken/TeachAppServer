from functools import wraps

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from server.models import User


class BaseAdminHandler(SessionMixin, RequestHandler):
    user = None


def admin_require(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        s = args[0]
        token_id = s.get_cookie('token-id')
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
