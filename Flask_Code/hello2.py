from flask import Flask, Blueprint

app = Flask(__name__)

app.config.from_pyfile('setting.py')
user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def user_profile():
    return 'user_profile'


@app.route("/")
def index():
    print(app.config['SECERET_KEY'])
    return "hello！"


app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run()
