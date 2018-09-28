from server.handlers.api.msg import UnreadMsgHandler, QuestionMsgHandler, \
    QuestionUserMsgHandler, JobMsgHandler, JobUserMsgHandler
from server.handlers.api.msg import UserMsgHandler
from server.handlers.api.order import OrderDetailHandler
from server.handlers.api.order import OrderHandler
from server.handlers.api.question import AnswerKeywordsDetailHandler
from server.handlers.api.question import AnswerKeywordsHandler
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
    (r'/api/msg/question/([0-9]+)', QuestionMsgHandler),
    (r'/api/msg/question/([0-9]+)/user/([0-9]+)', QuestionUserMsgHandler),
    (r'/api/msg/job', JobMsgHandler),
    (r'/api/msg/job/([0-9]+)/user/([0-9]+)', JobUserMsgHandler),
    (r'/api/orders', OrderHandler),
    (r'/api/orders/([0-9]+)', OrderDetailHandler),
    (r'/api/answer_keywords', AnswerKeywordsHandler),
    (r'/api/answer_keywords/([0-9]+)', AnswerKeywordsDetailHandler),
]
