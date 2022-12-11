# flask工程搭建和配置

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

app = Flask(__name__)
#装饰器的作用是将路由映射到视图函数index

@app.route( ' / ')
def index( ):
return 'Hello world'

 <!--Flask应用程序实例的run方法启动WEB服务器-->

if __name__ == "__mian__":

app.run()

### （1）初始化参数

####  import_name:

。Flask程序所在的包(模块)，传__name__就可以

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

app = Flask(__name__)

app.config.from_object(Defaultconfig)

app.route("/")
def index( ) :
	print(app.config[ ' SECRET_KEY'])
	return "hello world"

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
  export FLASK_ENV=production运行在生产模式，未指明则默认为此方式
  export FLASK_ENV=development运行在开发模式



# 路由与蓝图

## 1 路由



### 查询路由信息

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
return json. dumps({rule. endpoint: rule.rule for rule in rules _iterator})

### 请求方式

GET

OPTIONS(自带)  ->  简化版的GET请求 用于询问服务器接口的信息
比如接口允许的请求方式 允许的请求源头域名		

HEAD(自带)  简化版的GET请求
只返回GET请求处理时的响应头，不返回响应体

利用**methods参数**可以自己指定一个接口的请求方式
@app.route(" / itcast1", methods=["POST"])
def view_func_1():
	return "hello world 1"
@app.route(" /itcast2", methods= ["GET","POST"])
def view_func_2( ):
	return "hello world 2"



##  2 蓝图

在Flask中，使用蓝图Blueprint来分模块组织管理。
蓝图实际可以理解为是一个存储一组视图方法的容器对象，其具有如下特点:

一个应用可以具有多个Blueprint
可以将一个Blueprint注册到任何一个未使用的URL下比如“/user”、“Igoods"
Blueprint可以单独具有自己的模板、静态文件或者其它的通用操作方法，它并不是必须要实现应用的视图和函数的
在一个应用初始化时，就应该要注册需粟使用的Blueprint
但是一个Blueprint并不是一个完整的应用，它不能独立于应用运行，而必须要注册到某一个应用中。

### 使用蓝图可以分为三个步骤

1.创建一个蓝图对象
user_bp=Blueprint( 'user' ,__name__)
2.在这个蓝图对象上进行操作,注册路由,指定静态文件夹,注册模版过滤器
@user_bp.route(' / ')
def user_profile( ):
	return 'user_profile'
3.在应用对象上注册这个蓝图对象
app.register_blueprint(user_bp)
同级文件可以直接注册，在目录中的话需要先导入再注册
4.添加蓝图访问前缀
user_bp=Blueprin('user', __name__, url_prefix='user')

### 蓝图内部静态文件

和应用对象不同，蓝图对象创建时不会默认注册静态目录的路由。
需要我们在创建时指定 static_folder参数。

下面的示例将蓝图所在目录下的static_admin目录设置为静态目录
admin=Blueprint("admin",__name__,static_folder='static_admin')
app.register_blueprint(admin,url_prefix=' / admin ')

现在就可以使用/admin/static_admin/<filename>访问static_admin目录下的静态文件了。
也可通过static_url_path改变访问路径
admin = Blueprint("admin"，__name__,static_folder='static_admin ' , static_url_path='/lib')app.register_blueprint(admin,url_prefix= ' / admin ' )

### 蓝图内部模板目录

蓝图对象默认的模板目录为系统的模版目录，可以在创建蓝图对象时使用template_folder关键字参数设置模板目录
admin = Blueprint( ' admin ' ,__name__,template_folder='my_templates ')

# 请求和响应



## 处理请求

### 需求

在视图编写中需要读取客户端请求携带的数据时，如何才能正确的取出数据呢?
请求携带的数据可能出现在HTTP报文中的不同位置，需要使用不同的方法来获取参数。

### 转换器

例如，有一个请求访问的接口地址为/users/123，其中123实际上为具体的请求参数，表明请求123号用户的信息。此时如何从url中提取出123的数据?
Flask不同于Django直接在定义路由时编写正则表达式的方式，而是采用转换器语法:

@app.route( '/users/<user_id>')
def user_info(user_id ):
	print(type(user_id))
	return 'hello user {}'.format(user_id)

此处的<>即是一个转换器，默认为字符串类型，即将该位置的数据以字符串格式进行匹配、并以字符串数据类型类型、 user_id为参数名传入视图。



Flask也提供其他类型的转换器
DEFAULT_CONVERTERS = {
'default ': Unicodeconverter,
'string ':UnicodeConverter,
'any ':AnyConverter,
' path ': PathConverter,
'int ':IntegerConverter,
'float':FloatConverter,
' uuid ' :UUIDConverter,
}

将上面的例子以整型匹配数据，可以如下使用:
@app.route( '/users/<intluser_id>')
def user_info(user_id):
	print(type(user_id ))
	return 'hello user {]} '.format(user_id)

@app.route( ' /users/< int(min=1):user_id > ')
def user_info(user_id ):
	print(type(user_id))
	return 'hello user {} '.format(user_id)

### 定义方法

自定义转换器主要做3步
1.创建转换器类，保存匹配时的正则表达式

from werkzeug . routing import BaseConverter
class Mobileconverter(BaseConverter):
	"""
	手机号格式
	"""
	regex = r' 1[3-9] \d{9}'

注意regex名字固定

2.将自定义的转换器告知Flask应用
app = Flask(__name__)
#将自定义转换器添加到转换器字典中，并指定转换器使用时名字为:mobile app.url_map.converters [ ' mobile ' ] = Mobileconverter

3.在使用转换器的地方定义使用

@app.route( ' /sms_codes/<mobile:mob_num >')
def send_sms_code( mob_num ) :
	return 'send sms code to {i} '.format(mob_num)

2.其他参数
如果想要获取其他地方传递的参数，可以通过Flask提供的request对象。
不同位置的参数都存放在request的不同属性中。
属性		说明
data		记录请求的数据，并转换为字符串
form		记录请求中的表单数据
args		记录请求中的查询参数
cookies	记录请求中的cookie信息
headers	记录请求中的报文头
method	记录请求使用的HTTP方法
url	记录请求的URL地址
files	记录请求上传的文件

## 处理响应

### 需求

如何在不同的场景里返回不同的响应信息?

### 1 返回模板 render_template

使用render_template方法渲染模板并返回
例如，新建一个模板index.html
**模板文件需要放在templates模板文件目录里才能读取到**

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
我的模板html内容
<br/>{{my_str}}
<br/>{{my_int}}
</body>
</html>
from flask import render_template
@app.route('/')
def index():
	mstr = 'Hello黑马程序员'
	mint = 10
	return render_template( 'index.html', my_str=mstr, my_int=mint)



### 2 重定向

from flask import redirect

@app.route( '/demo2 ' )
def demo2( ) :
	return redirect( 'http: //www.itheima. com ')



### 3 返回JSON

from flask import jsonify

@app.route( ' /demo3 ')
def demo3():
	json_dict = {
	"user_id" :10,
	"user_name" : "laowang"
	}
	return jsonify(json_dict)

·return json.dumps()

·return jsonify

​	转换成json格式字符串
​	设置了响应头Content-Type:application/json

### 4自定义状态码和响应头

#### 1)元组方式

可以返回一个元组，这样的元组必须是**(response, status, headers)**的形式，且至少包含一个元素。status值会覆盖状态代码, headers可以是一个列表或字典，作为额外的消息标头值。
@app.route( ' /demo4 ' )
def demo4( ):
	#return '状态码为666',666
	return '状态码为 666'， 666， {'Itcast': 'Python'}



#### 2)make_response方式

@app.route( ' /demo5 ' )
def demo5( ):
	resp = make_response( 'make response测试')
	resp.headers ["Itcast"] =“Python"
	resp.statusI=“404 not found"
	return resp

## Cookie

设置
from flask import Flask, make_response

app = Flask( __name___)

@app.route( '/cookie ')
def set_cookie( ) :
	resp = make_response( 'set cookie ok ')
	resp.set_cookie( 'username ' , 'itcast ')
	return resp

设置有效期
@app.route( ' /cookie ')
def set_cookie( ) :
	response = make_response( ' hello world ')
	response.set_cookie('username','itheima',max_age=3600)
	return response

读取
from flask import request

@app.route( '/get_cookie ' )
def get_cookie( ) :
	resp = request.cookies.get( 'username ' )
	return resp

删除
from flask import request
@app.route( ' /delete_cookie ' )
def delete_cookie( ) :
	response = make_response('helloworld')
	response.delete_cookie( 'username ' )
	return response
实现原理：修改cookie的有效期

## Session

通过秘钥加密保存会话数据，并将会话数据保存到cookie中

session的使用需要先设置SECRET_KEY
class DefaultConfig(object):
	SECRET_KEY = 'fih9fh9eh9gh2 '

app. config.from_object(DefaultConfig)

或者直接设置
app.secret_key='xihwidfw9efw '

### 设置

from flask import session

@app.route( ' /set_session')
def set_session( ) :
	session[ 'username ' ] = 'itcast'
	return 'set session ok'

### 读取

@app.route( '/get_session' )
def get_session( ) :
	username = session. get( 'username ' )
	return 'get session username {} '.format(username)

# 请求钩子与上下文

## 异常处理

### HTTP异常主动抛出

​	abort方法

​		抛出一个给定状态代码的HTTPException或者 指定响应，例如	想要用一个页面未找到异常来终止请求，你可以调用abort（404）

​	参数：
​		code-HTTP的错误状态码

#abort（400）
abort(500)
抛出状态码的话，只能抛出HTTP协议的错误状态码



### 捕获错误

 errorhandler装饰器
 	注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
·参数:
		code_or_exception - HTTP的错误状态码或指定异常
·例如统一处理状态码为500的错误给用户友好的提示:
@app.errorhandler(500)
def internal_server_error(e):
	return '服务器搬家了'

·捕获指定异常

@app.errorhandler(zeroDivisionError)
def zero_division_error(e):
	return '除数不能为0'

## 中间件说明（请求钩子）

请求的处理过程pre_process -> view -> after_process

request请求支持处理流程
middleware1.pre_process() -> m2.pre_process() -> m3.pre_process()->view()
 -> m3.after_process() -> m2.after_process() -> m1.after_process()

中间件处理 不区分具体是哪个视图，对所有视图通通生效

在客户端和服务器交互的过程中，有些准备工作或扫尾工作需要处理，比如:
·在请求开始时，建立数据库连接;
·在请求开始时，根据需求进行权限校验;
·在请求结束时，指定数据的交互格式;

为了让每个视图函数避免编写重复功能的代码，Flask提供了通用设施的功能，即请求钩子。

请求钩子是通过装饰器的形式实现，Flask支持如下四种请求钩子:
. before_first_request
		在处理第一个请求前执行. 

before_request
		在每次请求前执行
		如果在某修饰的函数中返回了一个响应，视图函数将不再被调用

after_request
		如果没有抛出错误，在每次请求后执行。
		接受一个参数:视图函数作出的响应
		在此函数中可以对响应值在返回之前做最后一步修改处理。
		需要将参数中的响应在此参数中进行返回

teardown_request:
		在每次请求后执行
		接受一个参数:错误信息，如果有相关错误抛出

```python
#在第一次请求之前调用，可以在此方法内部做一些初始化操作
@app.before_first_request
def before_first_request():
    print ( "before_first_request")
#在每一次请求之前调用，这时候已经有请求了，可能在这个方法里面做请求的校验
#如果请求的校验不成功，可以直接在此方法中进行响应，直接return之后那么就不会执行视图函数
@app.before_request
def before_request():
    print( "before_request")
#if请求不符合条件:
#return "la9wang"
#在执行完视图函数之后会调用，并且会把视图函数所生成的响应传入,可以在此方法中对响应做最后一步统一的处理
@app.after_request
def after_request(response):
    print( "after_request")
    response.headers ["Content-Type"] = "application/json"
    return response
#请每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息@app.teardown_request
def teardown_request(response):
    print( "teardown_request")
 
```



## 上下文

### 请求上下文

思考︰在视图函数中，如何取到当前请求的相关数据?比如︰请求地址，请求方式，cookie等等在flask中，可以直接在视图函数中使用request 这个对象进行获取相关数据，而request就是请的对象，保存了当前本次请求的相关数据，请求上下文对象有:request、session
request
	封装了HTTP请求的内容，针对的是http请求。
	举例: user = request.args.get('user')，获取请求的参数。
session
	用来记录请求会话中的信息，针对的是用户信息。举例: session['name'] = user.id，可以信息。还可以通过session.get('name')获取用户信息。



### 2应用上下文(application context)

它的字面意思是应用上下文，但它不是一直存在的，它只是request context中的一个对app的代理人谓local proxy。它的作用主要是帮助request 获取当前的应用，它是伴request而生，随request而灭应用上下文对象有:current_app，g

#### current_app

应用程序上下文,用于存储应用程序中的变量，可以通过curgent_app.name打印当前app的名称，也可以current_app中存储一些变量，例如∶
·应用的启动脚本是哪个文件，启动时指定了哪些参数
·加载了哪些配置文件，导入了哪些配置
·连了哪个数据库
·有哪些public的工具类、常量
·应用跑在哪个机器上，IP多少，内存多大

示例



作用
current_app就是当前运行的flask app，在代码不方便直接操作flask的app对象时，可以操作current_app 就等价于操作flask app对象

#### g对象

g作为 flask程序全局的一个临时变量，充当中间媒介的作用，我们可以通过它在一次请求调用的多个函数间传递一些数据。每次请求都会重设这个变量。

示例

from flask import Flask, g

app = Flask(__name__)

def db_query ( ):
	user_id = g.user_id
	user_name = g.user_name
	print( 'user_id={(}user_name={}'.format(user_id,user_name))

@app.route( ' / ')
def get_user_profile():
	g.user_id = 123
	g.user_name = 'itcast'db_query()
	return 'hello world '

## g对象与请求钩子综合案例

### 需求

构建认证机制
对于特定视图可以提供强制要求用户登录的限制
	对于所有视图，无论是否强制要求用户登录，都可以在视图中尝试获取用户认证后的身份信息

分析
特定强制需求->装饰器
所有视图的需求->请求钩子

请求->请求钩子（尝试判断用户的身份 对于未登录用户不做处理  放行)   用g对象保存用户身份信息
g.user_id = 1232   g.user_id =None
->普通视图处理g.user_id i
->强制登录视图->装饰器

示例代码

```python
from flask import Flask,request,abort,current_app,g


app = Flask(__name__)
#请求钩子（尝试判断用户的身份对于未登录用户不做处理放行)用g对象保存用户身份信息
@app.before_request
def authentication():
    """
    利用before_request请求钩子，在进入所有视图前先尝试判断用户身份
    :return: 
    """
    #TOD0此处利用鉴权机制（如cookie、session、jwt等）鉴别用户身份信息#if已登录用户，用户有身份信息
    g.user_id = 123
    # else未登录用户，用户无身份信息
    # g.user_id =None
    
    
#强制登录装饰器
def login_required (func):
    def wrapper(*arg,**kwargs):
        #判断用户是否登录
        if g.user_id is None:
            abort(401)
        else:
        # 已登录
        	return func( *args,**kwargs)
    return wrapper


@app.route('/profile')
@login_required
def get_user_profile():
    return 'user profile page user_id={} '.format(g.user_id)
```



## 3 app_context request_context

思考
在Flask程序未运行的情况下，调试代码时需要使用current_app . g .request这些对象，会不会有问题﹖该如何使用?
app_context t
app_context为我们提供了应用上下文环境，允许我们在外部使用应用上下文current_app
、g
可以通过with语句进行使用>>>

>>>from flask import Flask>>>app = Flask( ' ')

.>>>app.redis_cli = 'redis client'

.>>>from flask import current_app

.>>>current_app.redis_cli  #错误，没有上下文环境

报错

.>>>Yith app.app_context():    #借助with语句使用app_context创建应用上下文
.>>>print(current_app.redis_cli)
redis client

### request_context

request_context为我们提供了请求上下文环境，允许我们在外部使用请求上下文 request , session
可以通过with语句进行使用



# ORM数据库操作

## Flask连接MySQL数据库

```python
from flask import Flask
from Flask-SQLAlchemy import SQLAlchemy
# NySQL监听的端口号，默认3306PORT = 3306
# 连接MySQL的用户名，读者用自己设置的USERNAME = "root"
# 连接MySQL的密码，读者用自己的PASSWORD = "root"
# MySQL上创建的数据库名称
DATABASE = "database_learn"l
app.config[ 'SQLALCHENY_DATABASE_URI' ] = f"mysql+pymysql://{USERNANE}:{PASSWORD}Q{HOSTNANE}:{PORT}/{DATABASE} ?charset=utf8"
# 在app.config中设置好连接数据库的信息，#然后使用SQLAlchemy ( app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息
db = SQLAlchemy(app)
```

测试数据库连接

```python
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute("select 1")
        print(rs.fetchone()) # (1,)
```

## ORM数据库增删改查操作

创建ORM模型

```python
class User(db.Model) :
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True，autoincrement=True)
    # varchar, null=0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100),nullable=False

with app.app_context():                         
	db.create_all() # 将ORM模型映射到数据库中                  
```

添加数据

```python
app.route("/user/add")
def add_user():
    # 1．创建ORM对象
    user = User(username="法外狂徒张三", password='111111')
    # 2．将ORM对象添加到db.session中
    db.session.add(user)
    # 3．将db.session中的改变同步到数据库中
    db.session.commit()
    return"用户创建成功!"
```

查找数据

```python
app.route("/user/query")
def query_user():
    # 1. get查找:根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}: {user.username}-{user.password}" )
    # 2. filter_by查找
    # Query:类数组
    users = User.query.filter_by(username="法外狂徒张三")
    for user in users:
        print(user.username)]return“数据查找成功!"
```

数据修改

```python
app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="法外狂徒张三").first()
    user.password = "222222"
    db.session.commit()
    return '数据修改成功!'
```

数据删除

```python
app.route( '/user/delete' )
def delete_user():
    #1．查找
    user = User.query.get(1)
    #2．从db.session中删除
    db.session.delete(user)
    # 3．将db.session中的修改，同步到数据库中
    db.session.commit()
    return"数据删除成功!
```

## ORM外键操作

```python
class Article(db. Model) :
    __tablename__ = "article"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #添加作者的外键
    author_id = db.Column(db.Integer, db.Foreignkey("user.id"))
    # 直接实现查找操作，同时自动在user中创建articles属性
    author = db.relationship( "User", backbref="articles")


article = Article(title="Flask学习大纲"，content="Flaskxxxx")
# article.author_id = user.id
# user = User.query.get(article.author_id)
# article.author =User.query.get(article.author_id)
print(article.author)

```

```python
# 创建文章
app.route( "/article/add")
def article_add():
    article1 = Article(title="Flask学习大纲"，content="FlaskxxxX")
    article1.author = User.query.get(2)
    article2 = Article(title="Django学习大纲"，content="Django最全学习大纲")
    article2.author = User.query.get(2)
    #添加到session中
    db.session.add_all([article1,article2])#同步session中的数据到数据库中
    db.session.commit()
    return "文章添加成功!"
```

```python
# 通过user查找文章
app.route( "/article/query")
def query_article():
    user = User.query.get(2)
    for article in user.articles:
    print(article.title)
    return"文章查找成功!"
```

#ORM模型映射成表的三步

1. flask db init:这步只需要执行一次

2. flask db migrate:识别ORM模型的改变，生成迁移脚本
3. flask db upgrade :运行迁移脚本，同步到数据库中

migrate = Migrate(app, db)
