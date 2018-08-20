import json

from sqlalchemy import and_
from sqlalchemy import or_
from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Msg


class UnreadMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.receiver == self.user.id,
            Msg.unread == 1
        )
        self.write({
            "msg": [
                m.get_info() for m in msgs
            ]
        })


class UserMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, user_id=None):
        with self.make_session() as session:
            msgs = session.query(Msg).filter(or_(
                and_(
                    Msg.receiver == user_id,
                    Msg.sender == self.user.id
                ),
                and_(
                    Msg.receiver == self.user.id,
                    Msg.sender == user_id
                )
            ))

            self.write({
                "msg": [
                    m.get_info() for m in msgs 
                ]
            })

    @coroutine
    @auth_require
    def put(self, receiver):
        body = json.loads(self.request.body.decode('utf-8'))
        msg = body.get("msg")

        receiver = msg['receiver']
        content = msg['content']

        with self.make_session() as session:
            msg = Msg(sender=self.user.id, receiver=receiver,
                      content=content)
            session.add(msg)
            session.flush()
            session.refresh(msg)
            self.write({"msg": msg.get_info()})

    @coroutine
    @auth_require
    def post(self, sender):
        with self.make_session() as session:
            msgs = session.query(Msg).filter(
                Msg.receiver == self.user.id,
                Msg.sender == sender
            )
            for msg in msgs:
                msg.unread = 0
            return {
                "success": "All massages marked read."
            }
