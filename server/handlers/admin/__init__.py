from server.handlers.admin.index import IndexHandler
from server.handlers.admin.user import LoginHandler
from server.handlers.admin.user import TokenListHandler

admin_handers = [
    (r'/admin', IndexHandler),
    (r'/admin/login', LoginHandler),
    (r'/admin/token', TokenListHandler),
]
