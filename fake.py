from models import DeclarativeBase
from models import User
from models import TeacherJob


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


def fake_data(session_factory):
    DeclarativeBase.metadata.create_all(session_factory.engine)
    session = session_factory.make_session()

    fake_user(session)

    session.commit()
    session.close()
