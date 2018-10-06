import os

from tornado.options import define

define("database_url",
       default="mysql+pymysql://root:aaaaaa@localhost/my_db?charset=utf8",
       help="Main user DB")

define("enable_fake_data",
       type=bool,
       default=False,
       help="enable fake data")

root_path = os.path.dirname(os.path.dirname(__file__))
static_path = os.path.join(root_path, "static")
web_app_path = os.path.join(root_path, "app")
upload_path = os.path.join(root_path, "uploads")
