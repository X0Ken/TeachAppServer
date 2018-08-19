import json

from sqlalchemy import and_
from sqlalchemy import or_

from server.models import Msg
from server.test import TestBase


class TestMsg(TestBase):

    def get_unread_count(self, receiver, sender=None):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.receiver == receiver,
            Msg.unread == 1
        )
        if sender:
            msgs = msgs.filter(Msg.sender == sender)
        count = msgs.count()
        return count

    def get_msg_count(self, user1_id, user2_id):
        session = self.session
        count = session.query(Msg).filter(or_(
            and_(Msg.receiver == user1_id, Msg.sender == user2_id),
            and_(Msg.receiver == user2_id, Msg.sender == user1_id)
        )).count()
        return count

    def test_unauth(self):
        response = self.fetch('/api/msg')
        self.assertEqual(response.code, 401)

    def test_list_unread(self):
        user = self.get_user()
        count = self.get_unread_count(user.id)
        response = self.fetch('/api/msg',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertGreater(count, 0)
        self.assertEqual(len(json.loads(response.body)['msg']), count)

    def test_msg_with_user(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        self.assertGreater(count, 0)
        self.assertEqual(len(json.loads(response.body)['msg']), count)

    def test_msg_read(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_unread_count(user1.id, user2.id)
        self.assertGreater(count, 0)
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              method="POST",
                              body=json.dumps({}),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        count = self.get_unread_count(user1.id, user2.id)
        self.assertEqual(count, 0)

    def test_msg_put(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        msg_info = {
            "sender": user1.id,
            "receiver": user2.id,
            "content": "是"
        }
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              method="PUT",
                              body=json.dumps({
                                  "msg": msg_info
                              }),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        c2 = self.get_msg_count(user1.id, user2.id)
        self.assertEqual(count+1, c2)
