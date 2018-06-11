import json
import uuid
import copy

from models import User
from tests import TestBase


class TestUser(TestBase):

    def test_user_get(self):
        response = self.fetch('/users/af71d42c091c426eb33982bf83779a75')
        self.assertEqual(response.code, 200)
        body = {
            "user": {
                "id": "af71d42c091c426eb33982bf83779a75",
                "username": "testuser"
            }
        }
        self.assertDictEqual(json.loads(response.body), body)

    def test_token_by_password(self):
        req_body = {
            "auth": {
                "type": "password",
                "username": "testuser",
                "password": "password",
            }
        }
        res_body = {
            "token": {
                'id': 'id',
                'token_id': "id",
                'role': 'user',
                'username': 'testuser'
            }
        }
        response = self.fetch('/token', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertListEqual(list(res_body.keys()), list(
            json.loads(response.body).keys()))
        self.assertListEqual(sorted(res_body['token'].keys()),
                             sorted(json.loads(response.body)['token'].keys()))

    def test_token_by_token(self):
        user = self.add_user()

        req_body = {
            "auth": {
                "type": "token",
                "token_id": user['token_id'],
            }
        }
        res_body = {
            "token": {
                'token_id': 'id',
                'role': 'user',
                'username': 'testuser',
                'id': 'id'
            }
        }
        response = self.fetch('/token', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertListEqual(list(res_body.keys()), list(
            json.loads(response.body).keys()))
        self.assertListEqual(sorted(res_body['token'].keys()),
                             sorted(json.loads(response.body)['token'].keys()))
        self.remove_user(user['id'])

    def test_user_property(self):
        user = self.add_user()
        req_body = {
            "property": {
                "a": "a",
                "b": "b",
            }
        }
        res_body = copy.deepcopy(req_body)
        response = self.fetch('/users/{}/property'.format(user['id']), method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertDictEqual(req_body, res_body)
        self.remove_user(user['id'])
