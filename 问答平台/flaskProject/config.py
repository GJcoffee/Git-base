
# 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "zlckqa"
USERNAME = 'root'
PASSWORD = ' root'
DB_URI = 'mysql+pymysql://{}{}@{}{}{}?charset=utf8 '.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEHY_DATABASE_URI = DB_URI

