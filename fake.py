from models import DeclarativeBase
from models import User
from models import TeacherJob, Teacher, Question


def fake_user(session):
    user = session.query(User).filter_by(
        uuid="af71d42c091c426eb33982bf83779a75").first()
    if not user:
        user = User(uuid="af71d42c091c426eb33982bf83779a75", username="testuser",
                    password="password", role="user", token_id='96da3aee6b6e47b98f08664abfbc599a')
        session.add(user)
    user = session.query(User).filter_by(
        uuid="370707741a0c41ef9d0e6a7d1fe2c043").first()
    if not user:
        user = User(uuid='370707741a0c41ef9d0e6a7d1fe2c043', username="testadmin",
                    password="password", role="admin")
        session.add(user)


def fake_teacher(session):
    user = session.query(User).filter_by(
        uuid="af71d42c091c426eb33982bf83779a76").first()
    if not user:
        user = User(uuid="af71d42c091c426eb33982bf83779a76", username="王老师",
                    password="password", role="user", token_id='af71d42c091c426eb33982bf83779a76')
        session.add(user)
        info = {
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
            "uuid": "af71d42c091c426eb33982bf83779a76"
        }
        teacher = Teacher(**info)
        session.add(teacher)

    user = session.query(User).filter_by(
        uuid="af71d42c091c426eb33982bf83779a77").first()
    if not user:
        user = User(uuid="af71d42c091c426eb33982bf83779a77", username="李老师",
                    password="password", role="user", token_id='af71d42c091c426eb33982bf83779a77')
        session.add(user)
        info = {
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
            "uuid": "af71d42c091c426eb33982bf83779a77"
        }
        teacher = Teacher(**info)
        session.add(teacher)


def fake_question(session):
    q = session.query(Question).filter_by(
        uuid="af71d42c091c426eb33982bf83779b77").first()
    if not q:
        info = {
            "uuid": "af71d42c091c426eb33982bf83779b77",
            "pay": "66",
            "context": "怎么做红烧肉",
            "keywords": "厨艺"
        }
        q = Question(**info)
        session.add(q)

    q = session.query(Question).filter_by(
        uuid="af71d42c092c426eb33982bf83779b77").first()
    if not q:
        info = {
            "uuid": "af71d42c092c426eb33982bf83779b77",
            "pay": "66",
            "context": "怎么计算三角形面积",
            "keywords": "数学"
        }
        q = Question(**info)
        session.add(q)


def fake_data(session_factory):
    DeclarativeBase.metadata.create_all(session_factory.engine)
    session = session_factory.make_session()

    fake_user(session)
    fake_teacher(session)
    fake_question(session)

    session.commit()
    session.close()
