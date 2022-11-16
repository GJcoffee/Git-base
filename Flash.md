## 1 flask框架

核心  Werkzerug + Jinja2

轻->只提供核心(视图、请求、响应的处理)

## 2 框架对比

重量级的框架:为方便业务程序的开发，提供了丰富的工具、组件，如Django
轻量级的框架∶只提供Web框架的核心功能，自由、灵活、高度定制，如Flask、Tornado

问题:

1.DJango与Flask谁好?

2.对比一下两个框架?
只有更合适的→轻重对比->框架选择上∶

自由、灵活、高度定制->Flask
快速实现业务、不考虑技术选型，越简单直接越好-> Django

## 3 工程搭建

创建helloworld.py文件
#导入Flask类
from flask import Flask

#Flask类接收一个参数

app = Flask(__name___)
#装饰器的作用是将路由映射到视图函数index@app.route( ' / ')
def index( ):
return 'Hello world'

 <!--Flask应用程序实例的run方法启动WEB服务器-->

if __name__ == "__mian__":

app.run()

### （1）初始化参数

####  import_name:

。Flask程序所在的包(模块)，传_name__就可以

。其可以决定Flask 在访问静态文件时查找的路径

#### static_url_path

。静态文件访问路径，可以不传，默认为︰/ + static_folder

#### static_folder

。静态文件存储的文件夹，可以不传，默认为static

#### template_foldert

。模板文件存储的文件夹，可以不传，默认为templates

### （2）工程配置的加载方式

####   从配置对象加载

class Defaultconfig(object):
"""默认配置"“"""
    SECRET_KEY ='TPmi4aLWRbyVq8zu9v82dwYW1'

app = Flask(__name_)

app.config.fom_object(Defaultconfig)

app.route("/")
def index( ) :
	print(app.config[ ' SECRET_KEY'])return "hello world"

应用场景:
作为默认配置写在程序代码中
可以继承

class Developmentonfig(DefaultConfig):
	DEBUG=True

优点：继承->复用

缺点：敏感数据暴露

#### 从配置文件中加载

app.config.from_pyfile(配置文件)

新建一个配置交件setting.py
SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1 '

在Flask程序文件中

app = Flask(__name__)

app.config.from_pyfile( 'setting.py ' )

@app.route("/")
def index():
	print(app.config [ 'SECRET_KEY'])

​	return "hello world"
应用场景︰
在项目中使用固定的配置文件

优点：独立文件 保护敏感数据

缺点：不能继承 文件路径固定 不灵活

#### 从环境变量中加载

通俗的理解，环境变量就是我们设置在操作系统中，由操作系统代为保存的变量值

在Linux系统中设置和读取环境变量的方式如下:

export 变量名=变量值  # 设置
echo $变量名  # 读取

#例如

export ITCAST=python 

echo $ITCAST

Flask使用环境变量加载配置的本质是通过环境变量值找到配置文件，再读取配置文件的信息，其使用方式为
app.config.from_envvar( '环境变量名')

环境变量的值为配置文件的绝对路径

先在终端中执行如下命令
export PROJECT_SETTING='~/setting.py'

再运行如下代码
app = Flask(__name__)

app.config.Jrom_envvar( ' PROJECT_SETTING ', silent=True)

app.route("/")
def index():

​	print(app.comfig['SECRET_KEY'])

优点：独立文件 保护敏感数据 文件路径不固定 灵活

缺点：不方便 要记得设置环境变量

#### 项目中的常用方式

使用工厂模式创建Flask app，并结合使用配置对象与环境变量加载配置
·使用配置对象加载默认配置
·使用环境变量加载不想出现在代码中的敏感配置信息
def create_flask_app( config ):
"""
创建Flask应用
: param config:配置对象

: return: Flask应用

"""
	app = Flask( __name__)
	app.config.from_object(config)
#从环境变量指向的配置文件中读取的配置信息会覆盖掉从配置对象中加载的同名		

​	app.config.from_envvar( "PROJECT_SETTING", silent=True)

​	return app

class DefaultConfig(object):
"""默认配置"""
	SECRET_KEY = 'itcast1'
	class DevelopmentConfig (DefaultConfig):
	DEBUG=True
	app = create_flask_app( DefaultConfig)p = create_flask_app(DevelopmentConfig)

app.route("/")
	def index ( ):
	print(app.config [ ' SECRET_KEY ' ])return "hello world"

### （3）app.run参数

可以指定运行的主机IP地址，端口，是否开启调试模式
app.run(host="0.0.0.0"", port=5000, debug = True)
关于DEBUG调试模式
1.程序代码修改后可以自动重启服务器
2.在服务器出现相关错误的时候可以直接将错误信息返回到前端进行展示



## 开发服务器启动方式

### 1 终端启动

$ export FLASK_APP=helloworld

$ flask run

* Running on http://127.0.0.1:5000/
  说明
  ·环境变量FLASK_APP指明flask的启动实例
  · flask run -h 0.0.0.0 -p 8000绑定地址端口

  . flask run --help获取帮助
  ·生产模式与开发模式的控制通过FLASK_ENV环境变量指明
  oexport FLASK_ENV=production运行在生产模式，未指明则默认为此方式oexport FLASK_ENV=development运行在开发模式



## 路由与蓝图

### 路由

#### 1.查询路由信息

命令行方式：

​	flask routes

在程序中获取:

​		在应用中的url_map属性中保存着整个Flask应用的路由映射信息，可以通过读取这个属性获取路由信息
print(app.url_map)

如果想在程序中遍历路由信息，可以采用如下方式
for rule in app.url_map.iter_rules ( ):
print( 'name=f} path={} '.format(rule.endpoint,rule.rule))

需求:
通过访问/地址，以json的方 式返回应用内的所有路由信息
实现
@app. route('/')
def route_ _map() :
"""
主视图，返回所有视图网址
"""
rules_ iterator = app.url_ _map. iter_ rules()
return json. dumps({rule. endpoint: rule.rule for rule in rules_ _iterator})

### 请求方式

GET

OPTIONS(自带)  ->  简化版的GET请求 用于询问服务器接口的信息
比如接口允许的请求方式 允许的请求源头域名		

HEAD(自带)  简化版的GET请求
只返回GET请求处理时的响应头，不返回响应体

利用**methods参数**可以自己指定一个接口的请求方式
@app.route(" / itcast1", methods=["POST"])def view_func_1():
return "hello world 1"
@app.route(" /itcast2", methods= ["GET","POST"])def view_func_2( ):
return "hello world 2"



## 蓝图

在Flask中，使用蓝图Blueprint来分模块组织管理。
蓝图实际可以理解为是一个存储一组视图方法的容器对象，其具有如下特点:

一个应用可以具有多个Blueprint
可以将一个Blueprint注册到任何一个未使用的URL下比如“/user”、“Igoods"
Blueprint可以单独具有自己的模板、静态文件或者其它的通用操作方法，它并不是必须要实现应用的视图和函数的
在一个应用初始化时，就应该要注册需粟使用的Blueprint
但是一个Blueprint并不是一个完整的应用，它不能独立于应用运行，而必须要注册到某一个应用中。



