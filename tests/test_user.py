import json
import uuid

from models import User
from tests import TestBase


class TestUser(TestBase):
    def add_user(self):
        session = self.session
        user = User(uuid=uuid.uuid4().hex, username=uuid.uuid4().hex,
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
