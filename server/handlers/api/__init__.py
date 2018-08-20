from server.handlers.api.msg import UnreadMsgHandler
from server.handlers.api.msg import UserMsgHandler
from server.handlers.api.question import QuestionDetailHandler
from server.handlers.api.question import QuestionHandler
from server.handlers.api.teacher import TeacherDetailHandler
from server.handlers.api.teacher import TeacherHandler
from server.handlers.api.teacher import TeacherJobDetailHandler
from server.handlers.api.teacher import TeacherJobHandler
from server.handlers.api.user import TokenHandler
from server.handlers.api.user import UserDetailHandler
from server.handlers.api.user import UserHandler
from server.handlers.api.user import UserPropertyHandler

api_handers = [
    (r'/api/teachers', TeacherHandler),
    (r'/api/teachers/([0-9]+)', TeacherDetailHandler),
    (r'/api/teacherjobs', TeacherJobHandler),
    (r'/api/teacherjobs/([0-9]+)', TeacherJobDetailHandler),
    (r'/api/users', UserHandler),
    (r'/api/users/([0-9]+)', UserDetailHandler),
    [r'/api/users/([0-9]+)/property', UserPropertyHandler],
    (r'/api/token', TokenHandler),
    (r'/api/questions', QuestionHandler),
    (r'/api/questions/([0-9]+)', QuestionDetailHandler),
    (r'/api/msg', UnreadMsgHandler),
    (r'/api/msg/([0-9]+)', UserMsgHandler),
]
