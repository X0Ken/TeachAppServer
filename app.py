import json
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from tornado_sqlalchemy import (SessionMixin, as_future, declarative_base,
                                make_session_factory)


define("database_url",
       default="mysql+pymysql://root:aaaaaa@localhost/my_db?charset=utf8",
       help="Main user DB")


DeclarativeBase = declarative_base()

AVALIBLE_ROLE = ['teach', 'student', 'administrator']
AVALIBLE_METHOD = ['remote', 'home']
AVALIBLE_GENDER = ['male ', 'female']
AVALIBLE_EDUCATION = ['Undergraduate', 'master', 'PhD']


class User(DeclarativeBase):
    __tablename__ = 'users'

    uuid = Column(String(32), primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(255))
    token_id = Column(String(255))


class Job(DeclarativeBase):
    __tablename__ = 'jobs'

    uuid = Column(String(32), primary_key=True)
    # 授课方式
    method = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(String(255))
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))

    deleted = Column(BigInteger, default=0)
    hidded = Column(BigInteger, default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)


class IndexHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        self.write('Hello Tom!')


class UserRegHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        self.write("""
<form method="post">
 First name:<br>
<input type="text" name="username">
<br>
 Password:<br>
<input type="password" name="password">
<br><br>
<input type="submit" value="Submit">
</form> 
            """)

    @coroutine
    def post(self):
        username = self.get_argument('username', default="", strip=True)
        password = self.get_argument('password', default="", strip=True)

        user = User(username=username, password=password)

        with self.make_session() as session:
            session.add(user)
        self.redirect('/user/login')


class UserLoginHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        err = self.get_argument('err', default='none')
        if err == "user":
            msg = "username not found"
        elif err == "pass":
            msg = "password error"
        else:
            msg = ""

        self.write("""
{}
<form method="post">
 User name:<br>
<input type="text" name="username">
<br>
 Password:<br>
<input type="password" name="password">
<br><br>
<input type="submit" value="Submit">
</form> 
            """ % msg)

    @coroutine
    def post(self):
        username = self.get_argument('username', default="", strip=True)
        password = self.get_argument('password', default="", strip=True)

        with self.make_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                if password == user.password:
                    self.set_cookie("username", username)
                    self.redirect('/user')
                else:
                    self.redirect('/user/login?err=pass')
            else:
                self.redirect('/user/login?err=user')


class UserLogoutHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        self.clear_cookie("username")
        self.redirect('/user/login')


class UserHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        username = self.get_cookie("username")
        if username:
            login = '<a href="/user/logout">login out</a>'
        else:
            login = '<a href="/user/login">login</a>'

        self.write("""
            Hello {} !<br/>
            {}
            """.format(username, login))


class TokenHandler(RequestHandler, SessionMixin):
    def get_token(self, user):
        return {
            "token": {
                "id": user.token_id,
                "username": user.username,
                "role": user.role,
            }
        }

    def auth_password(self, auth):
        username = auth.get('username')
        password = auth.get('password')
        user_id = None

        with self.make_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and password == user.password:
                user.token_id = uuid.uuid4().hex
                user_id = user.uuid

        print("user {}".format(user_id))
        if not user_id:
            self.set_status(401)
            self.write({
                "error": "User not found!"
            })
            return

        with self.make_session() as session:
            user = session.query(User).filter_by(uuid=user_id).first()
            self.write(self.get_token(user))

    def auth_token(self, auth):
        token_id = auth.get('token_id')

        with self.make_session() as session:
            user = session.query(User).filter_by(token_id=token_id).first()

            if not user:
                self.set_status(401)
                self.write({
                    "error": "User not found!"
                })
                return

            self.write(self.get_token(user))

    @coroutine
    def post(self):
        body = json.loads(self.request.body)
        auth = body.get("auth")
        auth_type = auth.get('type')
        if auth_type == "password":
            self.auth_password(auth)
        elif auth_type == "token":
            self.auth_token(auth)


class JobHandler(RequestHandler, SessionMixin):
    def get_job(self, job):
        return {
            "uuid": job.uuid,
            "method": job.method,
            "gender": job.gender,
            "school": job.school,
            "highest_education": job.highest_education,
            "pay": job.pay,
            "region": job.region,
            "subject": job.subject,
            "time": job.time,
            "create_at": job.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @coroutine
    def get(self):
        with self.make_session() as session:
            jobs = session.query(Job).filter_by(deleted=0).all()
            jobs = (self.get_job(job) for job in jobs)
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods',
                            'POST, GET, OPTIONS')
            self.write({
                "jobs": [job for job in jobs]
            })

    @coroutine
    def post(self):
        job_uuid = uuid.uuid4().hex
        body = json.loads(self.request.body)
        job = body.get("job")
        with self.make_session() as session:
            job = Job(uuid=job_uuid, **job)
            session.add(job)
        with self.make_session() as session:
            job = session.query(Job).filter_by(uuid=job_uuid).first()

            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers",
                            "x-requested-with, Content-Type")
            self.set_header('Access-Control-Allow-Methods',
                            'POST, GET, OPTIONS')
            self.write({"Job": self.get_job(job)})

    @coroutine
    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write("")


class AsyncWebRequestHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        with self.make_session() as session:
            count = yield as_future(session.query(User).count)

        self.write('{} users so far!'.format(count))


def fake_data(session_factory):
    DeclarativeBase.metadata.create_all(session_factory.engine)
    session = session_factory.make_session()

    user = session.query(User).filter_by(
        uuid="af71d42c091c426eb33982bf83779a75").first()
    if not user:
        user = User(uuid="af71d42c091c426eb33982bf83779a75", username="testuser",
                    password="password", role="user")
        session.add(user)
    user = session.query(User).filter_by(
        uuid="370707741a0c41ef9d0e6a7d1fe2c043").first()
    if not user:
        user = User(uuid='370707741a0c41ef9d0e6a7d1fe2c043', username="testadmin",
                    password="password", role="admin")
        session.add(user)

    session.commit()


if __name__ == '__main__':
    options.database_url = 'sqlite+pysqlite:///sqlite.db'
    session_factory = make_session_factory(options.database_url)
    fake_data(session_factory)

    Application([
        (r'/', IndexHandler),
        (r'/jobs', JobHandler),
        (r'/user', UserHandler),
        (r'/token', TokenHandler),
        (r'/user/reg', UserRegHandler),
        (r'/user/login', UserLoginHandler),
        (r'/user/logout', UserLogoutHandler),
    ], session_factory=session_factory, cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
        autoreload=True
    ).listen(8888)

    IOLoop.current().start()
