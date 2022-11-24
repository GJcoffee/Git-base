from flask import Flask, g, session
import config

from exts import db, mail
from models import UserModel
from flask_migrate import Migrate

from Blueprints.qa import qa_bp
from Blueprints.auth import auth_bp

# 与app相关的配置
app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# 数据库相关操作
db.init_app(app)
migrate = Migrate(app, db)
"""
flask db init
flask db migrate
flask db upgrate
"""

# 邮箱操作
mail.init_app(app)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        g.user = user
    else:
        g.user = None


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
