import json
from flask import Flask, render_template
from BP import user_bp


app = Flask(__name__)
# 导入目录文件中的蓝图
app.register_blueprint(user_bp)


# 模板响应
@app.route('/html')
def deal_html():
    mstr = '!!!'
    mint = 10
    return render_template('index.html', my_str=mstr, my_int=mint)


# 转换器测试
@app.route('/user/<user_id>')
def user_info(user_id):
    return f'user_id:{user_id}'


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
