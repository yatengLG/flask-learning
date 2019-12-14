# 第三章.模板

**入口为hello.py** 直接运行即可

## 3.1 Jinja
### 3.1.1 渲染模板

默认情况下，Flask 在程序文件夹中的 templates 子文件夹中寻找模板。

Flask 提供的 render_template 函数把 Jinja2 模板引擎集成到了程序中。
render_template 函数的第一个参数是模板的文件名。随后的参数都是键值对。


### 3.1.2 变量
在模板中使用的 {{ name }} 结构表示一个变量，它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取。

Jinja2 能识别所有类型的变量，甚至是一些复杂的类型，例如列表、字典和对象。
如：
```html
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```

另外，模板支持**过滤器**，过滤器可以对传入的变量进行修改。
例子： 过滤器capitalize 首字母大写形式显示变量 name 的值
```text
Hello, {{ name|capitalize }}
```

Jinja2变量过滤器：

|过滤器名    |说明|
|:----:     |:----:|
|safe       |渲染值时不转义,需要显示变量中存储的HTML代码时,就可使用safe过滤器|
|capitalize |把值的首字母转换成大写，其他字母转换成小写|
|lower      |把值转换成小写形式|
|upper      |把值转换成大写形式  |
|title      |把值中每个单词的首字母都转换成大写|
|trim       |把值的首尾空格去掉|
|striptags  |渲染之前把值中所有的 HTML 标签都删掉|


### 3.1.3 控制结构
Jinja2 提供了多种控制结构，可用来改变模板的渲染流程。

下例展示了**条件控制**语句：
```text
{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

下例为**循环**语句：

```text
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

**宏**语句，类似于python中的函数：
```text
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}
<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>
```

可以将**宏**单独保存在一个新的文件中，在使用时导入：
```text
{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
    {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
```

**模板继承**则类似与python中的类：
首先创建一个名为 base.html 的基模板，
```html
<html>
<head>
    {% block head %}
    <title>{% block title %}{% endblock %} - My Application</title>
    {% endblock %}
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>
```
基模板中定义的**块**，可以在衍生模板中进行修改。上例定义了head、title 和 body 的块

在衍生模板中使用基模板：
```html
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style>
    </style>
{% endblock %}
{% block body %}
<h1>Hello, World!</h1>
{% endblock %}
```

extends 指令声明这个模板衍生自 base.html
值得注意的是，由于head块在基模板中不是空的，所以需要使用super()获取原先的内容.

## 3.2 使用Flask-Bootstrap 集成 Bootstrap

在flask模板中使用bootstrap最简单的方式为：使用一个名为 Flask-Bootstrap 的 Flask 扩展

安装： pip install flask-bootstrap

在user.html中使用flask-bootstrap模板：
```html
{% extends "bootstrap/base.html" %}

......
```
Jinja2 中的 extends 指令从 Flask-Bootstrap 中导入 bootstrap/base.html，从而实现模板继承。
Flask-Bootstrap 中的基模板提供了一个网页框架，引入了 Bootstrap 中的所有 CSS 和JavaScript 文件。

基模板中定义了可在衍生模板中重定义的块。block 和 endblock 指令定义的块中的内容可
添加到基模板中。

## 3.3 自定义错误页面

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

## 3.4 链接

任何具有多个路由的程序都需要可以连接不同页面的链接，例如导航条

在模板中直接编写简单路由的 URL 链接不难，但对于包含可变部分的动态路由，在模板
中构建正确的 URL 就很困难。而且，直接编写 URL 会对代码中定义的路由产生不必要的
依赖关系。如果重新定义路由，模板中的链接可能会失效。

为了避免这些问题，Flask 提供了 url_for() 辅助函数，它可以使用程序 URL 映射中保存
的信息生成 URL.

使用 url_for() 生成动态地址时，将动态部分作为关键字参数传入。例如，url_for
('user', name='john', _external=True) 的返回结果是 http://localhost:5000/user/john。

传入 url_for() 的关键字参数不仅限于动态路由中的参数。函数能将任何额外参数添加到
查询字符串中。例如，url_for('index', page=2) 的返回结果是 /?page=2。

## 3.5 静态文件
Web 程序不是仅由 Python 代码和模板组成。大多数程序还会使用静态文件，例如 HTML代码中引用的图片、JavaScript 源码文件和 CSS.

默认设置下，Flask 在程序根目录中名为 static 的子目录中寻找静态文件。
如果需要，可在static 文件夹中使用子文件夹存放文件。

## 3.6 使用Flask-Moment本地化日期和时间

