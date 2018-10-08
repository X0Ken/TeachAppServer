from server.handlers.api.msg import UnreadMsgHandler, QuestionMsgHandler, \
    QuestionUserMsgHandler, JobMsgHandler, JobUserMsgHandler
from server.handlers.api.msg import UserMsgHandler
from server.handlers.api.order import OrderDetailHandler, OrderJobHandler, \
    OrderQuestionHandler
from server.handlers.api.order import OrderHandler
from server.handlers.api.question import AnswerKeywordsDetailHandler
from server.handlers.api.question import AnswerKeywordsHandler
from server.handlers.api.question import QuestionDetailHandler
from server.handlers.api.question import QuestionHandler
from server.handlers.api.teacher import TeacherDetailHandler, \
    TeacherFilterByJobHandler
from server.handlers.api.teacher import TeacherHandler
from server.handlers.api.teacher import TeacherJobDetailHandler
from server.handlers.api.teacher import TeacherJobHandler
from server.handlers.api.user import TokenHandler, UserInfoHandler
from server.handlers.api.user import UserDetailHandler
from server.handlers.api.user import UserHandler
from server.handlers.api.user import UserPropertyHandler
from server.handlers.api.utils import FileHandler
from server.handlers.api import schools

api_handers = [
    (r'/api/teachers', TeacherHandler),
    (r'/api/teachers/([0-9]+)', TeacherDetailHandler),
    (r'/api/teachers/job/([0-9]+)', TeacherFilterByJobHandler),
    (r'/api/teacherjobs', TeacherJobHandler),
    (r'/api/teacherjobs/([0-9]+)', TeacherJobDetailHandler),
    (r'/api/users', UserHandler),
    (r'/api/users/([0-9]+)', UserDetailHandler),
    [r'/api/users/([0-9]+)/property', UserPropertyHandler],
    (r'/api/users/info', UserInfoHandler),
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
    (r'/api/orders/job/([0-9]+)', OrderJobHandler),
    (r'/api/orders/question/([0-9]+)', OrderQuestionHandler),
    (r'/api/answer_keywords', AnswerKeywordsHandler),
    (r'/api/answer_keywords/([0-9]+)', AnswerKeywordsDetailHandler),
    (r'/api/upload', FileHandler),
    (r'/api/schools', schools.SchoolsHandler),
]
