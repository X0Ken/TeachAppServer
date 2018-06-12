import uuid

from tornado.testing import AsyncHTTPTestCase

import app
from models import User


class TestBase(AsyncHTTPTestCase):
    def get_app(self):
        application = app.make_app()
        self.session = application.settings['session_factory'].make_session()
        return app.make_app()

    def add_user(self, user_id=None):
        if not user_id:
            user_id = uuid.uuid4().hex
        session = self.session
        user = User(uuid=user_id, username=uuid.uuid4().hex,
                    password="password", role="user", token_id=uuid.uuid4().hex)
        user_info = user.get_token_info()
        session.add(user)
        session.commit()
        return user_info

    def remove_user(self, user_id):
        session = self.session
        user = session.query(User).filter_by(uuid=user_id).first()
        session.delete(user)
        session.commit()
