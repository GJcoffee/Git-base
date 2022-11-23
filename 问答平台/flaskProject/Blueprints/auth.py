import random

from flask import Blueprint, render_template, request, jsonify
from exts import mail, db
from flask_mail import Message
import string
from models import EmailCaptchaModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/login")
def login():
    pass


# 渲染注册模板
@auth_bp.route('/register')
def register():
    return render_template(register.html)


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




