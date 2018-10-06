import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.handlers.admin.base import admin_require


class IndexHandler(BaseAdminHandler):

    @coroutine
    @admin_require
    def get(self):
        self.render("index/index.html")
