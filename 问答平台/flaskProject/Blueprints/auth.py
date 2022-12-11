import random

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string
from models import EmailCaptchaModel, UserModel
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                # 通过cookie保持登录的状态
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误!")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


@auth_bp.route("/login_out")
def login_out():
    return redirect(url_for('app.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 渲染注册模板
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        form = RegisterForm(request.form)
        if form.validate():  # 可自行调用相关验证器进行验证
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            # 将表单信息存储到数据库
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


# 邮件发送验证码功能
@auth_bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email?email=xxx@qq.com
    # 获取邮箱
    email = request.args.get('email')
    # 获取验证码
    source = string.digits*4
    captcha = ''.join(random.sample(source, 4))  # 从源码中随机取4位
    print(captcha)
    # 向获取的邮箱发送验证码
    massage = Message(subject='web注册验证码', recipients=[email], body=f'验证码为{captcha}')
    mail.send(massage)
    # 1.用memcached/redis 方式暂存 2.用数据库存储
    # 存入数据库
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # 格式{'code': 200/400/500, massage:"", data:{}}
    return jsonify({"code": 200, "massage": None, "data": None})
