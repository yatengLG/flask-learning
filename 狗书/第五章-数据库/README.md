# 第五章 数据库

## 5.1 SQL数据库

关系型数据库把数据存储在表中，表模拟程序中不同的实体。

表的列数是固定的，行数是可变的。列定义表所表示的实体的数据属性。

表中有个特殊的列，称为主键，其值为表中各行的唯一标识符。
表中还可以有称为外键的列，引用同一个表或不同表中某行的主键。
行之间的这种联系称为关系，这是关系型数据库模型的基础

## 5.2 NoSQL数据库

不遵循上节所述的关系模型的数据库统称为 NoSQL 数据库.

## 5.3 使用SQL还是NoSQL

SQL 数据库擅于用高效且紧凑的形式存储结构化数据。这种数据库需要花费大量精力保证数据的一致性。

NoSQL 数据库放宽了对这种一致性的要求，从而获得性能上的优势。

## 5.4 数据库抽象层代码包

一些数据库抽象层代码包供选择，例如 SQLAlchemy 和MongoEngine。
你可以使用这些抽象包直接处理高等级的 Python 对象，而不用处理如表、文档或查询语言此类的数据库实体。

SQLAlchemy ORM 支持很多关系型数据库引擎，包括流行的 MySQL、Postgres 和 SQLite。

## 5.5 使用Flask-SQLAlchemy管理数据库

本书选择使用的数据库框架是 Flask-SQLAlchemy，这个 Flask 扩展包装了 SQLAlchemy框架。

安装： ```pip install flask-sqlalchemy```

在 Flask-SQLAlchemy 中，数据库使用 URL 指定。

|数据库引擎|URL|
|:----:|:----:|
|MySQL          |mysql://username:password@hostname/database|
|Postgres       |postgresql://username:password@hostname/database|
|SQLite(Unix)   |sqlite:////absolute/path/to/database|
|SQLite(Windows)|sqlite:///c:/absolute/path/to/database| 

URL中，hostname表示MySql服务所在的主机，可以是本地主机，也可以是远程服务器。

database 表示要使用的数据库名。 

如果数据库需要进行认证，username 和 password 表示数据库用户密令。

示例代码：
```python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
```
db 对象是 SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了 Flask-SQLAlchemy提供的所有功能。

## 5.6 定义模型

模型这个术语表示程序使用的持久化实体.
在 ORM 中，模型一般是一个 Python 类，类中的属性对应数据库表中的列.

Flask-SQLAlchemy 创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，可用于定义模型的结构。

示例代码： hello.py中定义 Role 和 User 模型
```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    
    def __repr__(self):
        return '<User %r>'%self.username

```
类变量 __tablename__ 定义在数据库中使用的表名。

其余的类变量都是该模型的属性，被定义为 db.Column类的实例。

db.Column 类构造函数的第一个参数是数据库列和模型属性的类型。

常用的SQLAlchemy列类型:

|类型名|Python类型|说明|
|:----:|:----:|:----:|
|Integer        |int                |普通整数，一般是 32 位
|SmallInteger   |int                |取值范围小的整数，一般是 16 位
|BigInteger     |int                |或 long 不限制精度的整数 
|Float          |float              |浮点数
|Numeric        |decimal.Decimal    |定点数
|String         |str                |变长字符串
|Text           |str                |变长字符串，对较长或不限长度的字符串做了优化
|Unicode        |unicode            |变长 Unicode 字符串
|UnicodeText    |unicode            |变长 Unicode 字符串，对较长或不限长度的字符串做了优化
|Boolean        |bool               |布尔值
|Date           |datetime.date      |日期
|Time           |datetime.time      |时间
|DateTime       |datetime.datetime  |日期和时间
|Interval       |datetime.timedelta |时间间隔
|Enum           |str                |一组字符串
|PickleType     |任何Python对象      |自动使用 Pickle 序列化
|LargeBinary    |str                |二进制文件

常用的SQLAlchemy列选项

|选项名|说明|
|:----:|:----:|
|primary_key    |如果设为 True，这列就是表的主键|
|unique         |如果设为 True，这列不允许出现重复的值|
|index          |如果设为 True，为这列创建索引，提升查询效率|
|nullable       |如果设为 True，这列允许使用空值；如果设为 False，这列不允许使用空值|
|default        |为这列定义默认值|

**Flask-SQLAlchemy 要求每个模型都要定义主键，这一列经常命名为 id。**

## 5.7 关系

关系型数据库使用关系把不同表中的行联系起来。

一对多关系在模型类中的表示方法如示例：
```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>'%self.username
        
```

关系使用 users 表中的外键连接了两行.
添加到User模型中的role_id列被定义为外键，就是这个外键建立起了关系.
传给db.ForeignKey()的参数'roles.id'表明，这列的值是roles表中行的id值.

添加到 Role 模型中的 users 属性代表这个关系的面向对象视角。
对于一个Role类的实例，其users属性将返回与角色相关联的用户组成的列表。
db.relationship()的第一个参数表明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。
db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。
这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值。

常用的SQLAlchemy关系选项：

|选项名|说明|
|:----:|:----:|
|backref        |在关系的另一个模型中添加反向引用|
|primaryjoin    |明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定|
|lazy           |指定如何加载相关记录。可选值有 select（首次访问时按需加载）、immediate（源对象加载后就加载）、joined（加载记录，但使用联结）、subquery（立即加载，但使用子查询），noload（永不加载）和 dynamic（不加载记录，但提供加载记录的查询|
|uselist        |如果设为 Fales，不使用列表，而使用标量值|
|order_by       |指定关系中记录的排序方式|
|secondary      |指定多对多关系中关系表的名字|
|secondaryjoin  |SQLAlchemy 无法自行决定时，指定多对多关系中的二级联结条件|

## 5.8 数据库操作

### 5.8.1 创建表

Flask-SQLAlchemy 根据模型类创建数据库。方法是使用 db.create_all()函数.

```python
from hello import db
db.create_all()
```

### 5.8.2 插入行

```python
from hello import Role, User
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)
```

通过数据库会话管理对数据库所做的改动.
在 Flask-SQLAlchemy 中，会话由 db.session表示。准备把对象写入数据库之前，先要将其添加到会话中.
```python
db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)
```
或者简写为：
```python
db.session.add_all([admin_role, mod_role, user_role,... ,user_john, user_susan, user_david])
```

为了把对象写入数据库，我们要调用 commit() 方法提交会话.
```python
db.session.commit()
```

数据库会话也可以回滚，添加到数据库会话中的所有对象都会还原到它们在数据库时的状态：
```python
db.session.rollback()
```

### 5.8.3 修改行
在数据库会话上调用 add() 方法也能更新模型。
```python
admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()
```

### 5.8.4 删除行
数据库会话还有个 delete() 方法。
```python
db.session.delete(mod_role)
db.session.commit()
```

**删除与插入和更新一样，提交数据库会话后才会执行**

### 5.8.5 查询行
Flask-SQLAlchemy 为每个模型类都提供了 query 对象。
最基本的模型查询是取回对应表中的所有记录:
```python
Role.query.all()
```
使用过滤器可以配置 query 对象进行更精确的数据库查询。下面这个例子查找角色为"User" 的所有用户
```python
User.query.filter_by(role=user_role).all()
```

```python
user_role = Role.query.filter_by(name='User').first()
```

常用的SQLAlchemy查询过滤器:

|过滤器|说明|
|:----:|:----:|
|filter()       |把过滤器添加到原查询上，返回一个新查询|
|filter_by()    |把等值过滤器添加到原查询上，返回一个新查询|
|limit()        |使用指定的值限制原查询返回的结果数量，返回一个新查询|
|offset()       |偏移原查询返回的结果，返回一个新查询|
|order_by()     |根据指定条件对原查询结果进行排序，返回一个新查询|
|group_by()     |根据指定条件对原查询结果进行分组，返回一个新查询|

在查询上应用指定的过滤器后，通过调用 all() 执行查询，以列表的形式返回结果。
除了all() 之外，还有其他方法能触发查询执行。

常用的SQLAlchemy查询执行函数:

|方法|说明|
|:----:|:----:|
|all()          |以列表形式返回查询的所有结果|
|first()        |返回查询的第一个结果，如果没有结果，则返回 None|
|first_or_404() |返回查询的第一个结果，如果没有结果，则终止请求，返回 404 错误响应|
|get()          |返回指定主键对应的行，如果没有对应的行，则返回 None|
|get_or_404()   |返回指定主键对应的行，如果没找到指定的主键，则终止请求，返回 404 错误响应|
|count()        |返回查询结果的数量|
|paginate()     |返回一个 Paginate 对象，它包含指定范围内的结果|

关系和查询的处理方式类似：
```python
users = user_role.users
users[0].role
```
但是，执行 user_role.users 表达式时，隐含的查询会调用 all() 返回一个用户列表。
query 对象是隐藏的，因此无法指定更精确的查询过滤器。

修改了关系的设置，加入了 lazy = 'dynamic' 参数，从而禁止自动执行查询
```python
class Role(db.Model):
    # ...
    users = db.relationship('User', backref='role', lazy='dynamic')
    # ...
```

这样配置关系之后，user_role.users 会返回一个尚未执行的查询，因此可以在其上添加过滤器：
```python
user_role.users.order_by(User.username).all()
```


## 5.9 在视图函数中操作数据库

数据库操作可以直接在视图函数中进行.

下例展示了首页路由的新版本，已经把用户输入的名字写入了数据库：
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('index'))
        return render_template('index.html',form = form, name = session.get('name'),known = session.get('known', False))
```

在修改后的版本中，提交表单后。程序会使用filter_by查询过滤器在数据库中查询提交的名字。
变量know会被写入用户会话中，因此重定向之后，可以把数据传给模板，用来显示自定义的欢迎消息。

对应的模板新版本如下例：
```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Flasky{% endblock %}
{% block page_content %}
<div class="page-header">
    <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
    {% if not known %}
    <p>Pleased to meet you!</p>
    {% else %}
    <p>Happy to see you again!</p>
    {% endif %}
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
```

## 5.10　集成Python shell
每次启动 shell 会话都要导入数据库实例和模型，这真是份枯燥的工作。
为了避免一直重复导入，我们可以做些配置，让 Flask-Script 的 shell 命令自动导入特定的对象.

## 5.11 使用Flask-Migrate实现数据库迁移

有时需要修改数据库模型，而且修改之后还需要更新数据库.

仅当数据库表不存在时，Flask-SQLAlchemy 才会根据模型进行创建。
因此，更新表的唯一方式就是先删除旧表，不过这样做会丢失数据库中的所有数据。

更新表的更好方法是使用数据库迁移框架。
数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中。

SQLAlchemy 的主力开发人员编写了一个迁移框架，称为 Alembic

除了直接使用 Alembic 之外，Flask 程序还可使用 Flask-Migrate 扩展.
这个扩展对 Alembic 做了轻量级包装，并集成到 Flask-Script 中，所有操作都通过 Flask-Script 命令完成。

安装：```pip install flask-migrate```

```python
from flask.ext.migrate import Migrate, MigrateCommand
# ...
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
```

这部分完了在写.
