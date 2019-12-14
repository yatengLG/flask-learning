# 第四章 Web表单

**本例子入口为hello.py** 直接运行即可、

尽管 Flask 的请求对象提供的信息足够用于处理 Web 表单，但有些任务很单调，而且要重复操作。比如，生成表单的 HTML 代码和验证提交的表单数据。

Flask-WTF（http://pythonhosted.org/Flask-WTF/）扩展可以把处理 Web 表单的过程变成一种愉悦的体验。
这个扩展对独立的 WTForms（http://wtforms.simplecodes.com）包进行了包装，方便集成到 Flask 程序中

Flask-WTF安装：pip install flask-wtf

## 4.1 跨站请求伪造保护

默认情况下，Flask-WTF 能保护所有表单免受跨站请求伪造（Cross-Site Request Forgery，CSRF）的攻击。恶意网站把请求发送到被攻击者已登录的其他网站时就会引发 CSRF 攻击。

为了实现 CSRF 保护，Flask-WTF 需要程序设置一个密钥。Flask-WTF 使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪。

设置密钥的方法如下例所示：

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
```
app.config 字典可用来存储框架、扩展和程序本身的配置变量。
使用标准的字典句法就能把配置值添加到 app.config 对象中。
这个对象还提供了一些方法，可以从文件或环境中导入配置值

## 4.2 表单类

使用 Flask-WTF 时，每个 Web 表单都由一个继承自 Form 的类表示。
这个类定义表单中的一组字段，每个字段都用对象表示。
字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求

```python
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
 name = StringField('What is your name?', validators=[Required()])
 submit = SubmitField('Submit')
```
这个表单中的字段都定义为类变量，类变量的值是相应字段类型的对象。
上例中，NameForm 表单中有一个名为 name 的文本字段和一个名为 submit 的提交按钮.
StringField
类表示属性为 type="text" 的 <input> 元素。
SubmitField 类表示属性为 type="submit" 的<input> 元素。
字段构造函数的第一个参数是把表单渲染成HTML时使用的标号.

StringField 构造函数中的可选参数 validators 指定一个由验证函数组成的列表，
在接受用户提交的数据之前验证数据。验证函数 Required() 确保提交的字段不为空。

WTForms支持的HTML标准字段：

|字段类型                 |说明|
|:----:|:----:|
|StringField            |文本字段|
|TextAreaField          |多行文本字段
|PasswordField          |密码文本字段
|HiddenField            |隐藏文本字段
|DateField              |文本字段，值为 datetime.date 格式
|DateTimeField          |文本字段，值为 datetime.datetime 格式
|IntegerField           |文本字段，值为整数
|DecimalField           |文本字段，值为 decimal.Decimal
|FloatField             |文本字段，值为浮点数
|BooleanField           |复选框，值为 True 和 False
|RadioField             |一组单选框
|SelectField            |下拉列表
|SelectMultipleField    |下拉列表，可选择多个值
|FileField              |文件上传字段
|SubmitField            |表单提交按钮
|FormField              |把表单作为字段嵌入另一个表单
|FieldList              |一组指定类型的字段

WTForms 内建的验证函数:

|验证函数|说明|
|:----:|:----:|
|Email          |验证电子邮件地址
|EqualTo        |比较两个字段的值；常用于要求输入两次密码进行确认的情况
|IPAddress      |验证 IPv4 网络地址
|Length         |验证输入字符串的长度
|NumberRange    |验证输入的值在数字范围内
|Optional       |无输入值时跳过其他验证函数
|Required       |确保字段中有数据
|Regexp         |使用正则表达式验证输入值
|URL            |验证 URL
|AnyOf          |确保输入值在可选值列表中
|NoneOf         |确保输入值不在可选值列表中


## 4.3 把表单渲染成HTML
表单字段是可调用的，在模板中调用后会渲染成 HTML。
假设视图函数把一个NameForm实例通过参数 form 传入模板，在模板中可以生成一个简单的表单.
如下例所示：
```html
<form method="POST">
 {{ form.hidden_tag() }} 
 {{ form.name.label }} {{ form.name() }}
 {{ form.submit() }}
</form>
```
Flask-Bootstrap 提供了一个非常高端的辅助函数，
可以使用 Bootstrap 中预先定义好的表单样式渲染整个 Flask-WTF 表单，
而这些操作只需一次调用即可完成。使用 Flask-Bootstrap，
上述表单可使用下面的方式渲染:
```html
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
```
## 4.4 在视图中处理表单

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()   # 实例化表单
    if form.validate_on_submit():   # 如果数据通过了所有验证，validate_on_submit()返回True
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)
 
```

## 4.5 重定向和用户会话
最新版的 hello.py 存在一个可用性问题。用户输入名字后提交表单，
然后点击浏览器的刷新按钮，会看到一个莫名其妙的警告，要求在再次提交表单之前进行确认。

是因为刷新页面时浏览器会重新发送之前已经发送过的最后一个请求。如果这个
请求是一个包含表单数据的 POST 请求，刷新页面后会再次提交表单.

基于这个原因，最好别让 Web 程序把 POST 请求作为浏览器发送的最后一个请求.
这种需求的实现方式是，使用重定向作为 POST 请求的响应，而不是使用常规响应。
但这种方法会带来另一个问题。程序处理 POST 请求时，使用 form.name.data 获取用户输入的名字，可是一旦这个请求结束，数据也就丢失了。
这是就需要把数据存储到**用户会话**中，在请求之间`记住`数据.
默认情况下 **用户会话** 保存在客户端**cookie**中.使用设置的 SECRET_KEY 进行加密签名。如果篡改了 cookie 中的内容，签名就会失效，会话也会随之失效。

示例代码：
```python
from flask import Flask, render_template, session, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))
```
这个变量现在保存在用户会话中，即 session['name']，所以在两次请求之间也能记住输入的值.
redirect() 是个辅助函数，用来生成 HTTP 重定向响应.redirect() 函数的参数是重定向的 URL.
url_for() 函数的第一个且唯一必须指定的参数是端点名，即路由的内部名字。

## 4.6 Flask消息

请求完成后，有时需要让用户知道状态发生了变化。这里可以使用确认消息、警告或者错误提醒。
这种功能是 Flask 的核心特性.flash() 函数可实现这种效果

示例代码：
```python
from flask import Flask, render_template, session, redirect, url_for, flash
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'))
```

仅调用 flash() 函数并不能把消息显示出来，程序使用的模板要渲染这些消息。
最好在基模板中渲染 Flash 消息，因为这样所有页面都能使用这些消息。
Flask 把 get_flashed_messages() 函数开放给模板，用来获取并渲染消息.

示例代码： templates/base.html
```html
{% block content %}
<div class="container">
    {% for message in get_flashed_messages() %}
    <div class="alert alert-warning">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        {{ message }}
    </div>
    {% endfor %}
    {% block page_content %}{% endblock %}
</div>
{% endblock %}
```