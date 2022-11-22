from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


def datetime_format(value, format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)

app.add_template_filter(datetime_format,"dformat")



class User:
    def __init__(self,username,email):
        self.username = username
        self.email = email


@app.route('/')
def hello_world():
    user = User(username="知了", email="xx@qq.com")
    person = {
        "username": "张三",
        "email": "zhangsan@qq.com"
    }
    return render_template("index.html", user=user, person=person)


@app.route("/blog/<blog_id>")
def blog_detail(blog_id):
    return render_template("blog_detail.html", blog_id=blog_id, username="知了")

@app.route("/filter")
def filter_demo():
    user = User(username="知了xxxx", email="xx@qq.com")
    mytime = datetime.now()
    return render_template("filter.html", user=user, mytime=mytime)

@app.route("/control")
def control_statement():
    age = 18
    books = [{
        "name": "三国演义",
        "author": "罗贯中"
    },{
        "name": "水浒传",
        "author": "施耐庵"
    },]
    return render_template("control.html", age=age, books=books)


@app.route("/child1")
def child1():
    return render_template("child1.html")


@app.route("/child2")
def child2():
    return render_template("child2.html")


@app.route('/static')
def static_demo():
    return render_template("static.html")


if __name__ == '__main__':
    app.run()
