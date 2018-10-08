from server.handlers.admin.index import IndexHandler
from server.handlers.admin.jobs import JobsHandler
from server.handlers.admin.questions import QuestionsHandler
from server.handlers.admin.teachers import TeachersHandler
from server.handlers.admin.user import LoginHandler, UsersHandler, \
    UserInfosHandler
from server.handlers.admin.user import TokenListHandler
from server.handlers.admin import schools

admin_handers = [
    (r'/admin', IndexHandler),
    (r'/admin/login', LoginHandler),
    (r'/admin/token', TokenListHandler),
    (r'/admin/questions', QuestionsHandler),
    (r'/admin/jobs', JobsHandler),
    (r'/admin/teachers', TeachersHandler),
    (r'/admin/users', UsersHandler),
    (r'/admin/users/infos', UserInfosHandler),
    (r'/admin/schools', schools.SchoolsHandler),
    (r'/admin/schools/add', schools.SchoolAddHandler),
    (r'/admin/schools/delete', schools.SchoolDeleteHandler),
]
