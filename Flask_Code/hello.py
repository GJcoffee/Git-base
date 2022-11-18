import json
from flask import Flask
from BP import user_bp

app = Flask(__name__)
# 导入目录文件中的蓝图
app.register_blueprint(user_bp)


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
