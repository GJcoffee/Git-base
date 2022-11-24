# 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "Flask"
USERNAME = 'root'
PASSWORD = 'qfyn66HFJ'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '1909621145@qq.com'
MAIL_PASSWORD = 'tsdpjjpabxswdjhh'
MAIL_DEFAULT_SENDER = '1909621145@qq.com'
# tsdpjjpabxswdjhh 邮箱授权码

# 秘钥
SECRET_KEY = "jslfjkgdfgdfd"
