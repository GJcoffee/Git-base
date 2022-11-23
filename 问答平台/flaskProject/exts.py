# exts.py 这个文件存在的意义是为了解决循环引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
