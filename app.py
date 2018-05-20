from sqlalchemy import Column, BigInteger, String
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado_sqlalchemy import (as_future, declarative_base,
                                make_session_factory, SessionMixin)
from tornado.web import RequestHandler, Application

define("database_url", 
    default="mysql+pymysql://root:aaaaaa@localhost/my_db?charset=utf8", 
    help="Main user DB")


DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    type = Column(String(255))


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


class AsyncWebRequestHandler(RequestHandler, SessionMixin):
    @coroutine
    def get(self):
        with self.make_session() as session:
            count = yield as_future(session.query(User).count)

        self.write('{} users so far!'.format(count))


if __name__ == '__main__':
    session_factory = make_session_factory(options.database_url)
    DeclarativeBase.metadata.create_all(session_factory.engine)

    Application([
        (r'/', IndexHandler),
        (r'/user', UserHandler),
        (r'/user/reg', UserRegHandler),
        (r'/user/login', UserLoginHandler),
        (r'/user/logout', UserLogoutHandler),
    ], session_factory=session_factory, cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
    autoreload=True
    ).listen(8888)

    IOLoop.current().start()