from server.models import Msg
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
        "id": 1
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
        'method': "",
        'pay': "",
        'region': "",
        'school': "",
        'subject': "",
        'time': ""
    }
]

question_info_list = [
    {
        "id": 2,
        "asker": 2,
        "pay": "66",
        "content": "怎么做红烧肉",
        "keywords": "厨艺"
    },
    {
        "id": 1,
        "asker": 3,
        "pay": "66",
        "content": "怎么计算三角形面积",
        "keywords": "数学"
    }
]

msg_info_list = [
    {
        "id": 1,
        "sender": 2,
        "receiver": 3,
        "content": "您是这个方面的专家吗？"
    },
    {
        "id": 2,
        "sender": 3,
        "receiver": 2,
        "content": "是"
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


def insert_fake_data(session_factory):
    session = session_factory.make_session()

    fake_user(session)
    fake_teacher(session)
    fake_teacherjob(session)
    fake_question(session)
    fake_msg(session)

    session.commit()
    session.close()
