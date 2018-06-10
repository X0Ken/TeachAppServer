from tornado.testing import AsyncHTTPTestCase

import app


class TestBase(AsyncHTTPTestCase):
    def get_app(self):
        application = app.make_app()
        self.session = application.settings['session_factory'].make_session()
        return app.make_app()
