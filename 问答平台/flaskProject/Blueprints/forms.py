import wtforms
from wtforms.validators import Email, Length


# Form:用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(massage="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, massage="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, massage="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, massage="密码格式错误！")])
    #7:18
