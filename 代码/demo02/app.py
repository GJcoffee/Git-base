from flask import Flask, request

app = Flask(__name__)


# url: http[80]/https[443]://www.qq.com:443/path
# url与视图：path与视图

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/profile")
def profile():
    return "我是个人中心！"

@app.route("/blog/list")
def blog_list():
    return "我是博客列表！"

# 带参数的url：将参数固定到了path中
@app.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    return "您访问的博客是：%s" % blog_id


# 查询字符串的方式传参
# /book/list：会给我返回第一页的数据
# /book/list?page=2：获取第二页的数据
@app.route('/book/list')
def book_list():
    # arguments：参数
    # request.args：类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"您获取的是第{page}的图书列表！"



if __name__ == '__main__':
    app.run()
