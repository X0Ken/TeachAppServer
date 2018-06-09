import json

from tornado.testing import AsyncHTTPTestCase

import app


class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_homepage(self):
        response = self.fetch('/user/af71d42c091c426eb33982bf83779a75')
        self.assertEqual(response.code, 200)
        body = {
            "user": {
                "id": "af71d42c091c426eb33982bf83779a75",
                "username": "testuser"
            }
        }
        self.assertDictEqual(json.loads(response.body), body)
