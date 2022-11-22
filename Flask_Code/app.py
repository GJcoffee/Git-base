from flask import Flask, abort, g

app = Flask(__name__)


# 请求钩子
@app.before_request
def auther():
    g.user_id = 123


def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is None:
            abort(401)
        else:
            return func(*args, **kwargs)
    return wrapper()


@app.route('/profile')
@login_required
def get_user_profile():
    return 'user profile page user_id={}'.format(g.user_id)
