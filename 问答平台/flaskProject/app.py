from flask import Flask
from flask import render_template
# import config
#
# from exts import db
# from models import UserModel
# from flask_migrate import Migrate
#
# from Blueprints.qa import qa_bp
# from Blueprints.auth import auth_bp

# 与app相关的配置
app = Flask(__name__)
# # 绑定配置文件
# app.config.from_object(config)
# # 注册蓝图
# app.register_blueprint(qa_bp)
# app.register_blueprint(auth_bp)

# # 数据库相关操作
# db.init_app(app)
# migrate = Migrate(app, db)
"""
flask db init
flask db migrate
flask db upgrate
"""


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
