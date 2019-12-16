# 第七章 大型程序的结构

尽管在单一脚本中编写小型 Web 程序很方便，但这种方法并不能广泛使用。程序变复杂后，使用单个大型源码文件会导致很多问题.

在本章，我们将介绍一种使用包和模块组织大型程序的方式。

## 7.1 项目结构

Flask程序的基本结构如下所示：

```text
|- flasky
    |-app 
        |-templates
        |-static
        |-main
            |-__init__.py
            |-errors.py
            |-forms.py
            |-views.py
        |-__init__.py
        |-email.py
        |-models.py
    |-migrations/
    |-tests/
        |-__init__.py
        |-test*.py
    |-venv/
    |-requirements.txt
    |-config.py
    |-manage.py
```

有四个顶级文件夹：
* Falsk程序一般保存在app文件夹下
* migrations包含数据库迁移脚本
* tests文件夹中保存单元测试
* venv中包含了python环境

* manage.py用于启动程序以及其他的程序任务。
* requirements.txt 依赖项
* config.py配置

## 7.2 配置选项

程序经常需要设定多个配置。这方面最好的例子就是开发、测试和生产环境要使用不同的数据库，这样才不会彼此影响

## 7.3　程序包

程序包用来保存程序的所有代码、模板和静态文件。
可以把这个包直接称为 app，如果有需求，也可使用一个程序专用名字.

templates 和 static 文件夹是程序包的一部分，因此这两个文件夹被移到了 app 中。
数据库模型和电子邮件支持函数也被移到了这个包中，分别保存为 app/models.py 和 app/email.py。

### 7.3.1 使用程序工厂函数

在单个文件中开发程序很方便，但却有个很大的缺点，因为程序在全局作用域中创建，所以无法动态修改配置。
这一点对单元测试尤其重要，因为有时为了提高测试覆盖度，必须在不同的配置环境中运行程序。

这个问题的解决方法是延迟创建程序实例，把创建过程移到可显式调用的工厂函数中。

构造文件导入了大多数正在使用的 Flask 扩展。由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数。
create_app() 函数就是程序的工厂函数，接受一个参数，是程序使用的配置名。

配置类在 config.py 文件中定义，其中保存的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入程序。
程序创建并配置好后，就能初始化扩展了。在之前创建的扩展对象上调用 init_app() 可以完成初始化过程.

示例代码 app/__init__.py：程序包的构造文件
```python
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
def create_app(config_name):
 app = Flask(__name__)
 app.config.from_object(config[config_name])
 config[config_name].init_app(app)
 bootstrap.init_app(app)
 mail.init_app(app)
 moment.init_app(app)
 db.init_app(app)
 # 附加路由和自定义的错误页面
 return app
 
```
工厂函数返回创建的程序示例，不过要注意，现在工厂函数创建的程序还不完整，因为没有路由和自定义的错误页面处理程序。

## 7.3.2 在蓝本中实现程序功能

转换成程序工厂函数的操作让定义路由变复杂了。
在单脚本程序中，程序实例存在于全局作用域中，路由可以直接使用 app.route 修饰器定义。
但现在程序在运行时创建，只有调用 create_app() 之后才能使用 app.route 修饰器，
这时定义路由就太晚了。和路由一样，自定义的错误页面处理程序也面临相同的困难，
因为错误页面处理程序使用 app.errorhandler 修饰器定义。

**幸好 Flask 使用蓝本提供了更好的解决方法.**

蓝本和程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，
直到蓝本注册到程序上后，路由才真正成为程序的一部分。

和程序一样，蓝本可以在单个文件中定义，也可使用更结构化的方式在包中的多个模块中创建。
为了获得最大的灵活性，程序包中创建了一个子包，用于保存蓝本。

示例代码：
```python
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors
```

通过实例化一个 Blueprint 类对象可以创建蓝本。
这个构造函数有两个必须指定的参数： 蓝本的名字和蓝本所在的包或模块。

程序的路由保存在包里的 app/main/views.py 模块中.
而错误处理程序保存在 app/main/errors.py 模块中.
导入这两个模块就能把路由和错误处理程序与蓝本关联起来.

注意，这些模块在 app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，因为在views.py 和 errors.py 中还要导入蓝本 main。

蓝本在工厂函数 create_app() 中注册到程序上
```python
# app/_init_.py：
def create_app(config_name):
 # ...
 from .main import main as main_blueprint
 app.register_blueprint(main_blueprint)
 return app
```

