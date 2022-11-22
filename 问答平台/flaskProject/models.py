from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID 作为主键 自动增长
    username = db.Column(db.String(100), nullable=False)  # 用户名，不能为空
    password = db.Column(db.String(100), nullable=False)  # 密码
    email = db.column(db.String(100), nullable=False, unique=True)  # 邮箱不能为空 且唯一
    join_time = db.column(db.DateTime, default=datetime.now)  # 加入时间
