from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# pip install flask-migrate
from flask_migrate import Migrate


app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "root"
# MySQL上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


# 在app.config中设置好连接数据库的信息，
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# ORM模型映射成表的三步
# 1. flask db init：这步只需要执行一次
# 2. flask db migrate：识别ORM模型的改变，生成迁移脚本
# 3. flask db upgrade：运行迁移脚本，同步到数据库中



# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute("select 1")
#         print(rs.fetchone())  # (1,)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar, null=0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    signature = db.Column(db.String(100))


# user = User(username="法外狂徒张三", password='111111')
# sql: insert user(username, password) values('法外狂徒张三', '111111');

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # backref：会自动的给User模型添加一个articles的属性，用来获取文章列表
    author = db.relationship("User", backref="articles")


# article = Article(title="Flask学习大纲", content="Flaskxxxx")
# article.author_id = user.id
# user = User.query.get(article.author_id)
# article.author = User.query.get(article.author_id)
# print(article.author)
# sqlalchemy/flask

# user.articles


# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user/add")
def add_user():
    # 1. 创建ORM对象
    user = User(username="法外狂徒张三", password='111111')
    # 2. 将ORM对象添加到db.session中
    db.session.add(user)
    # 3. 将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功！"


@app.route("/user/query")
def query_user():
    # 1. get查找：根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}: {user.username}-{user.password}")
    # 2. filter_by查找
    # Query：类数组
    users = User.query.filter_by(username="法外狂徒张三")
    for user in users:
        print(user.username)
    return "数据查找成功！"


@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="法外狂徒张三").first()
    user.password = "222222"
    db.session.commit()
    return "数据修改成功！"


@app.route('/user/delete')
def delete_user():
    # 1. 查找
    user = User.query.get(1)
    # 2. 从db.session中删除
    db.session.delete(user)
    # 3. 将db.session中的修改，同步到数据库中
    db.session.commit()
    return "数据删除成功！"


@app.route("/article/add")
def article_add():
    article1 = Article(title="Flask学习大纲", content="Flaskxxxx")
    article1.author = User.query.get(2)

    article2 = Article(title="Django学习大纲", content="Django最全学习大纲")
    article2.author = User.query.get(2)

    # 添加到session中
    db.session.add_all([article1, article2])
    # 同步session中的数据到数据库中
    db.session.commit()
    return "文章添加成功！"


@app.route("/article/query")
def query_article():
    user = User.query.get(2)
    for article in user.articles:
        print(article.title)
    return "文章查找成功！"


if __name__ == '__main__':
    app.run()
