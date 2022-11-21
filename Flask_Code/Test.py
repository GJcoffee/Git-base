import json
from flask import Flask, render_template, redirect, url_for, jsonify, make_response, request, session, abort
from BP import user_bp

app = Flask(__name__)
# 导入目录文件中的蓝图
app.register_blueprint(user_bp)
# 设置session 秘钥
app.secret_key = 'sdfsdfsfdsdf'


@app.route('/')
def index():
    return 'hello！'


# 遍历路由
@app.route('/route')
def route_():
    print(app.url_map)
    for rule in app.url_map.iter_rules():
        print('name={} path={}'.format(rule.endpoint, rule.rule))
        rules_iterator = app.url_map.iter_rules()
        return json.dumps({f'{rule.endpoint}': rule.rule for rule in rules_iterator})


# 模板响应
@app.route('/html')
def deal_html():
    mstr = '!!!'
    mint = 10
    return render_template('index.html', my_str=mstr, my_int=mint)


@app.route('/redirect')  # 重定向失败
def redirect():
    return redirect(url_for('http://www.itheima.com'))


# 返回json
@app.route('/re_json')
def return_json():
    json_dict = {
        'user_id': 10,
        'user_name': 'laowang',
    }
    return jsonify(json_dict)


# 转换器测试
@app.route('/user/<user_id>')
def user_info(user_id):
    return f'user_id:{user_id}'


# 自定义状态码和响应头
# 元组方式
@app.route('/response_')
def response_():
    return '状态码为666', 666, {'ID': "python"}


# make_response方式
@app.route('/make_response')
def make_response_():
    resp = make_response('测试')
    resp.headers['head'] = 'python'
    resp.status = '404 not found'
    return resp


# 设置cookie
@app.route('/Cookie')
def set_cookie_():
    resn = make_response('set cookie ok')
    resn.set_cookie('username', 'this a cookie')
    return resn


# 设置cookie 有效期
@app.route('/cookie_1')
def set_cookie():
    response = make_response('cookie')
    response.set_cookie('username', '19096', max_age=3600)
    return response


# 读取cookie
@app.route('/get_cookie')
def get_cookie():
    resp = request.cookies.get('username')
    return resp


# 删除cookie
@app.route('/delete_cookie')
def delete_cookie():
    resn = make_response('删除cookie')
    resn.delete_cookie('username')
    return resn


# 设置session
@app.route('/set_session')
def set_session():
    session['username'] = 'HJ'
    return 'set session ok'


# 读取session
@app.route('/get_session')
def get_session():
    username = session.get('username')
    return "get session username {}".format(username)


# 错误捕获
@app.errorhandler(404)
def internal_server_error(e):
    return '请稍后再访问!'


# 请求钩子
