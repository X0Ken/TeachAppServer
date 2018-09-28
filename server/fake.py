from server.models import Msg, AnswerKeywords
from server.models import Order
from server.models import Question
from server.models import Teacher
from server.models import TeacherJob
from server.models import User

user_info_list = [
    {
        "id": 1,
        "username": "admin",
        "password": "password",
        "role": "admin",
        'pic': "/static/imgs/user1.jpg",
        "token_id": "96da3aee6b6e47b98f08664abfbc599a"
    },
    {
        "id": 2,
        "username": "user",
        "password": "password",
        "role": "user",
        'pic': "/static/imgs/user1.jpg",
        "token_id": "af71d42c091c426eb33982bf83779a75"
    },
    {
        "id": 3,
        "username": "user2",
        "password": "password",
        "role": "user",
        'pic': "/static/imgs/user2.jpg",
        "token_id": "370707741a0c41ef9d0e6a7d1fe2c043"
    },
    {
        "id": 4,
        "username": "老马",
        "password": "password",
        "role": "user",
        'pic': "/static/imgs/user2.jpg",
        "token_id": "370707741a0c41ef9d0e6a7d1fe2c043"
    }
]

teacher_info_list = [
    {
        "gender": "男",
        "highest_education": "博士",
        "idcard": "fdsdf",
        "method": "上门",
        "pay": "30-40",
        "region": "西城区",
        "school": "北京中央财经大学",
        "school_subject": "体育",
        "self_evaluate": "飞洒付付付付付付付付付付付付",
        "subject": "英语",
        "time": "下午",
        "id": 2
    },
    {
        "gender": "女",
        "highest_education": "硕士",
        "idcard": "fdsdf",
        "method": "网络",
        "pay": "30-40",
        "region": "西城区",
        "school": "北京中央财经大学",
        "school_subject": "体育",
        "self_evaluate": "飞洒付付付付付付付付付付付付",
        "subject": "英语",
        "time": "上午",
        "id": 3
    }
]

teacherjob_info_list = [
    {
        'id': 1,
        'gender': "a",
        'highest_education': "ed",
        'method': "远程",
        'pay': "100",
        'region': "北京",
        'school': "北京大学",
        'subject': "语文",
        'time': "下午",
        'provider': 2
    },
    {
        'id': 2,
        'gender': "a",
        'highest_education': "ed",
        'method': "上门",
        'pay': "50",
        'region': "海淀区",
        'school': "清华大学",
        'subject': "数学",
        'time': "中午",
        'provider': 4
    }
]

question_info_list = [
    {
        "id": 2,
        "asker_id": 2,
        "pay": "66",
        "content": "怎么做红烧肉",
        "keywords": "厨艺"
    },
    {
        "id": 1,
        "asker_id": 3,
        "pay": "66",
        "content": "怎么计算三角形面积",
        "keywords": "数学"
    }
]

msg_info_list = [
    {
        "id": 1,
        "sender_id": 3,
        "receiver_id": 2,
        "content": "您是这个方面的专家吗？",
        "typ": "question",
        "typ_id": 2,
    },
    {
        "id": 2,
        "sender_id": 3,
        "receiver_id": 2,
        "content": "这个我教你",
        "typ": "question",
        "typ_id": 2,
    },
    {
        "id": 3,
        "sender_id": 4,
        "receiver_id": 2,
        "content": "这个我会",
        "typ": "question",
        "typ_id": 2,
    },
    {
        "id": 4,
        "sender_id": 2,
        "receiver_id": 3,
        "content": "是",
        "typ": "question",
        "typ_id": 2,
    },
    {
        "id": 5,
        "sender_id": 2,
        "receiver_id": 3,
        "content": "您是这个方面的专家吗？",
        "typ": "job",
        "typ_id": 1,
    },
    {
        "id": 6,
        "sender_id": 2,
        "receiver_id": 3,
        "content": "你了解这方面的信息吗？",
        "typ": "job",
        "typ_id": 1,
    },
    {
        "id": 7,
        "sender_id": 2,
        "receiver_id": 4,
        "content": "在吗",
        "typ": "job",
        "typ_id": 1,
    },
    {
        "id": 8,
        "sender_id": 4,
        "receiver_id": 2,
        "content": "是",
        "typ": "job",
        "typ_id": 1,
    },
    {
        "id": 9,
        "sender_id": 4,
        "receiver_id": 3,
        "content": "是",
        "typ": "job",
        "typ_id": 2,
    },
    {
        "id": 10,
        "sender_id": 4,
        "receiver_id": 2,
        "content": "你周末有空吗？",
        "typ": "job",
        "typ_id": 2,
    },
]

order_info_list = [
    {
        'id': 1,
        'payer_id': 4,
        'payee_id': 3,
        'unit': "天",
        'unit_price': 1000,
        'number': 1,
        'amount': 1000,
        'typ': 'job',
        'typ_id': 2,
        'state': 'payed',
    },
    {
        'id': 2,
        'payer_id': 3,
        'payee_id': 2,
        'unit': "次",
        'unit_price': 1000,
        'number': 1,
        'amount': 1000,
        'typ': 'question',
        'typ_id': 2,
        'state': 'create',
    },
]

answer_keyword_info_list = [
    {
        "id": 1,
        "user_id": 2,
        "keyword": 'test',
    }
]


def fake_user(session):
    for user_info in user_info_list:
        user = session.query(User).filter_by(
            id=user_info['id']).first()
        if not user:
            user = User(**user_info)
            session.add(user)


def fake_teacher(session):
    for teacher_info in teacher_info_list:
        teacher = session.query(Teacher).filter_by(
            id=teacher_info['id']).first()
        if not teacher:
            teacher = Teacher(**teacher_info)
            session.add(teacher)


def fake_teacherjob(session):
    for job_info in teacherjob_info_list:
        job = session.query(TeacherJob).filter_by(
            id=job_info['id']).first()
        if not job:
            job = TeacherJob(**job_info)
            session.add(job)


def fake_question(session):
    for question_info in question_info_list:
        question = session.query(Question).filter_by(
            id=question_info['id']).first()
        if not question:
            question = Question(**question_info)
            session.add(question)


def fake_msg(session):
    for msg_info in msg_info_list:
        msg = session.query(Msg).filter_by(
            id=msg_info['id']).first()
        if not msg:
            msg = Msg(**msg_info)
            session.add(msg)


def fake_order(session):
    for order_info in order_info_list:
        order = session.query(Order).filter_by(
            id=order_info['id']).first()
        if not order:
            order = Order(**order_info)
            session.add(order)


def fake_answer_keyword(session):
    for answer_keyword_info in answer_keyword_info_list:
        answer_keyword = session.query(AnswerKeywords).filter_by(
            id=answer_keyword_info['id']).first()
        if not answer_keyword:
            answer_keyword = AnswerKeywords(**answer_keyword_info)
            session.add(answer_keyword)


def insert_fake_data(session_factory):
    session = session_factory.make_session()

    fake_user(session)
    fake_teacher(session)
    fake_teacherjob(session)
    fake_question(session)
    fake_msg(session)
    fake_order(session)
    fake_answer_keyword(session)

    session.commit()
    session.close()
