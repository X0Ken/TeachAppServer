
import os
import random
import string

from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Msg


class FileHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for x in
            range(6))
        final_filename = fname + extension
        output_file = open("uploads/" + final_filename, 'w')
        output_file.write(file1['body'])
        self.finish("file" + final_filename + " is uploaded")



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
            "msgs": [
                m.get_info() for m in msgs
            ]
        })
