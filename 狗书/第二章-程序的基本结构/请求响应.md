# 请求-响应循环

## 程序和请求上下文：

Flask从客户端收到请求时，需要视图函数处理请求。

视图函数接受信息的最简单的方式便是，将信息作为参数传递给视图函数。
但在复杂任务时，传入的信息不定，且量大。
使用参数传递的方式便不再实用。

**Flask使用上下文**作为全局变量，来让视图函数处理请求。

如下例代码：
```python
from flask import request

@app.route('/'):
def inde():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```
例子中，flask将request 当作全局变量使用。方便视图函数处理。
Falsk 使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程。

flask支持两种上下文：程序上下文和请求上下文。

|     变量名 |上下文类型|   说明  |
|   :----:  |:----:  | :----:|
|current_app|程序上下文|当前激活程序的程序实例|
|       g   |程序上下文|处理请求时用作临时存储的对象。每次请求都会重设这个变量|
|   request |请求上下文|请求对象，封装了客户端发出的 HTTP 请求中的内容|
|   session |请求上下文|用户会话，用于存储请求之间需要“记住”的值的词典|


## 请求调度
程序收到客户端发来的请求时，要找到处理该请求的视图函数。
URL 映射是 URL 和视图函数之间的对应关系。
Flask 使用 app.route 修饰器或者非修饰器形式的 app.add_url_rule() 生成映射.

## 请求钩子
有时在处理请求之前或之后执行代码会很有用.
例如，在请求开始时，我们可能需要创建数据库连接或者认证发起请求的用户。
为了避免在每个视图函数中都使用重复的代码，Flask 提供了注册通用函数的功能，注册的函数可在请求被分发到视图函数之前或之后调用.

**请求钩子使用修饰器实现**,支持以下 4 种钩子：

|变量名                  |说明|
|:----:|:----:|
|before_first_request   |注册一个函数，在处理第一个请求之前运行。|
|before_request         |注册一个函数，在每次请求之前运行。
|after_request          |注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
|teardown_request       |注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。


## 响应

Flask 调用视图函数后，会将其返回值作为响应的内容。
大多数情况下，响应就是一个简单的字符串，作为 HTML 页面回送客户端

视图函数返回的响应 还可以有 **状态码**以及**header**

如果不想返回由 1 个、2 个或 3 个值组成的元组，flask还可以返回Response对象。
通过make_response() 函数可接受 1 个、2 个或 3 个参数（和视图函数的返回值一样），并返回一个 Response 对象。
下例创建了一个响应对象，并设置了cookie:
```python
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>Hello World!<h1>')
    response.set_cookie('answer','42')
    return response
```

#### 重定向 
还有一种名为**重定向**的特殊响应。这种响应没有页面文档，只是告诉浏览器一个新地址用于加载新页面。
重定向经常使用 302 状态码表示，指向的地址由 Location 首部提供。

Flask 提供了 redirect() 辅助函数
```python
from flask import redirect

@app.route('/')
def index():
    return redirect('https://www.baidu.com/')
```

#### 错误处理
还有一种特殊的响应：**abort** ,用于处理错误。
下例中，如果URL中动态参数 id 对应的用户不存在，就返回状态码 404
```python

from flask import abort
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
```

