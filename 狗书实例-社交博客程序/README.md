# 实例-社交博客程序

# 第八章 用户认证

大多数程序都要进行用户跟踪。用户连接程序时会进行身份认证，通过这一过程，让程序知道自己的身份。程序知道用户是谁后，就能提供有针对性的体验。

## 8.1 Flask的认证扩展

本章介绍的认证方案使用了多个包，并编写了胶水代码让其良好协作。
本章使用的包列表如下：

* Flask-Login       管理已登录用户的用户会话
* Werkzeug          计算密码散列值并进行核对
* itsdangerous      生成并核对加密安全令牌

除了上述认证相关的包以外，本章还用到了如下常规用途的扩展：

* Falsk-Mail        发送与认证相关的电子邮件
* Flask-Bootstrap   HTML模板
* Flask-WTF         Web表单

## 8.2 密码安全性

想保证数据库中用户密码的安全，关键在于不能存储密码本身，而要存储密码的散列值。

计算密码散列值的函数接收密码作为输入，使用一种或多种加密算法转换密码，最终得到一个和原始密码没有关系的字符序列。
核对密码时，密码散列值可代替原始密码，因为计算散列值的函数是可复现的：只要输入一样，结果就一样。

### 使用Werkzeug实现密码散列

Werkzeug 中的 security 模块能够很方便地实现密码散列值的计算。

这一功能的实现只需要两个函数，分别用在注册用户和验证用户阶段。

* ```generate_password_hash(password, method=pbkdf2:sha1, salt_length=8)```

这个函数将原始密码作为输入，以字符串形式输出密码的散列值，输出的值可保存在用户数据库中。
method 和 salt_length 的默认值就能满足大多数需求。

* ```check_password_hash(hash, password)```

这个函数的参数是从数据库中取回的密码散列值和用户输入的密码。返回值为 True 表明密码正确。

示例代码：app/models.py
```python

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # ...
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        assert AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
```

## 8.3 创建认证蓝本

把创建程序的过程移入工厂函数后，可以使用蓝本在全局作用域中定义路由。

对于不同的程序功能，我们要使用不同的蓝本，这是保持代码整齐有序的好方法。

auth 蓝本保存在同名 Python 包中。蓝本的包构造文件创建蓝本对象，再从 views.py 模块中引入路由

示例代码 app/auth/__init__.py

```python
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

```
app/auth/views.py 模块引入蓝本，然后使用蓝本的 route 修饰器定义与认证相关的路由

添加了一个 /login 路由，渲染同名占位模板.
示例代码 app/auth/views.py：蓝本中的路由和视图函数

```python
from flask import render_template
from . import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html')
```

**注意，为 render_template() 指定的模板文件保存在 auth 文件夹中。这个文件夹必须在app/templates 中创建**

auth 蓝本要在 create_app() 工厂函数中附加到程序上.

示例代码 app/__init__.py：附加蓝本

```python

def create_app(config_name):
 # ...
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
```

注册蓝本时使用的 url_prefix 是可选参数。
如果使用了这个参数，注册后蓝本中定义的所有路由都会加上指定的前缀，
即这个例子中的 /auth。例如，/login 路由会注册成 /auth/login，
在开发 Web 服务器中，完整的 URL 就变成了 http://localhost:5000/auth/login

## 8.4 Flask-Login 认证用户

用户登录程序后，他们的认证状态要被记录下来，这样浏览不同的页面时才能记住这个状态。
Flask-Login 是个非常有用的小型扩展，专门用来管理用户认证系统中的认证状态，且不依赖特定的认证机制。

安装：``` pip install flask-login```

### 8.4.1 准备用于登录的用户模型

要想使用 Flask-Login 扩展，程序的 User 模型必须实现几个方法。
需要实现的方法如下表所示：

|方法|说明|
|:----:|:----:|
|is_authenticated() |如果用户已经登录，必须返回 True，否则返回 False|
|is_active()        |如果允许用户登录，必须返回 True，否则返回 False。如果要禁用账户，可以返回 False|
|is_anonymous()     |对普通用户必须返回 False|
|get_id()           |必须返回用户的唯一标识符，使用 Unicode 编码字符串|

这 4 个方法可以在模型类中作为方法直接实现，不过还有一种更简单的替代方案。
Flask-Login 提供了一个 UserMixin 类，其中包含这些方法的默认实现，且能满足大多数需求。

修改后的User模型为：app/models.py
```python

from flask-login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
```

示例中同时还添加了 email 字段。在这个程序中，用户使用电子邮件地址登录，因为相对于用户名而言，用户更不容易忘记自己的电子邮件地址。

Flask-Login 在程序的工厂函数中初始化

示例代码： app/__init__.py：初始化 Flask-Login
```python
from flask-login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
def create_app(config_name):
    # ...
    login_manager.init_app(app)
    # ...
```
LoginManager 对象的 session_protection 属性可以设为 None、'basic' 或 'strong'，以提供不同的安全等级防止用户会话遭篡改。
设为 'strong' 时，Flask-Login 会记录客户端 IP地址和浏览器的用户代理信息，如果发现异动就登出用户。
login_view 属性设置登录页面的端点。回忆一下，登录路由在蓝本中定义，因此要在前面加上蓝本的名字。

最后，Flask-Login 要求程序实现一个回调函数，使用指定的标识符加载用户。
这个函数的定义如示例所示：app/models.py

```python
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。
如果能找到用户，这个函数必须返回用户对象；否则应该返回 None。


### 8.4.2 保护路由

为了保护路由只让认证用户访问，Flask-Login 提供了一个 login_required 修饰器。
用法演示如下：
```python
from flask.ext.login import login_required
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
```

如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。

### 8.4.3 添加登录表单

呈现给用户的登录表单中包含一个用于输入电子邮件地址的文本字段、一个密码字段、一个'记住我'复选框 和 提交按钮。

这个表单使用 Flask-WTF 实现，代码如下：
```python
from flask_wtf import Form
from wtforms import StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me loggin in')
    submit = SubmitField('Log in')

```

电子邮件字段用到了 WTForms 提供的 Length() 和 Email() 验证函数。
PasswordField 类表示属性为 type="password" 的 <input> 元素。
BooleanField 类表示复选框。

登录页面使用的模板保存在 auth/login.html 文件中。
这个模板只需使用 Flask-Bootstrap 提供的 wtf.quick_form() 宏渲染表单即可。

### 8.4.4 登入用户

视图函数 login() 的实现如示例所示
app/auth/views.py
```python
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
```

这个视图函数创建了一个 LoginForm 对象.
当请求类型是 GET 时，视图函数直接渲染模板，即显示表单。
当表单在 POST 请求中提交时，Flask-WTF 中的 validate_on_submit() 函数会验证表单数据，然后尝试登入用户。

为了登入用户，视图函数首先使用表单中填写的 email 从数据库中加载用户。
如果电子邮件地址对应的用户存在，再调用用户对象的 verify_password() 方法，其参数是表单中填写的密码。
如果密码正确，则调用 Flask-Login 中的 login_user() 函数，在用户会话中把用户标记为已登录。

login_user() 函数的参数是要登录的用户，以及可选的“记住我”布尔值，“记住我”也在表单中填写。
如果值为 False，那么关闭浏览器后用户会话就过期了，所以下次用户访问时要重新登录。
如果值为 True，那么会在用户浏览器中写入一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。

用户访问未授权的 URL 时会显示登录表单，Flask-Login会把原地址保存在查询字符串的 next 参数中，这个参数可从 request.args 字典中读取。
如果查询字符串中没有 next 参数，则重定向到首页.
如果用户输入的电子邮件或密码不正确，程序会设定一个 Flash 消息，再次渲染表单，让用户重试登录.

### 8.4.5 登出用户

退出路由的实现如示例所示

app/auth/views.py
```python
from flask.ext.login import logout_user, login_required

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
```

为了登出用户，这个视图函数调用 Flask-Login 中的 logout_user() 函数，删除并重设用户会话。
随后会显示一个 Flash 消息，确认这次操作，再重定向到首页，这样登出就完成了。


### 8.4.6 测试登录

为验证登录功能可用，可以更新首页，使用已登录用户的名字显示一个欢迎消息。
模板中生成欢迎消息的部分如示例所示。

app/templates/index.html

```html
Hello,
{% if current_user.is_authenticated() %}
    {{ current_user.username }}
{% else %}
    Stranger
{% endif %}!
```
在这个模板中再次使用 current_user.is_authenticated() 判断用户是否已经登录。

## 8.5 注册新用户

如果新用户想成为程序的成员，必须在程序中注册，这样程序才能识别并登入用户。
程序的登录页面中要显示一个链接，把用户带到注册页面，让用户输入电子邮件地址、用户名和密码.

### 8.5.1 添加用户注册表单

app/auth/forms.py
```python
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', 
                            validators=[Required(), 
                                        Length(1, 64), 
                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
                                        
    password = PasswordField('Password', 
                              validators=[Required(), 
                                          EqualTo('password2', message='Passwords must match.')])
                                          
    password2 = PasswordField('Confirm password', validators=[Required()])
    
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
```

这个表单使用 WTForms 提供的 Regexp 验证函数，确保 username 字段只包含字母、数字、下划线和点号。
这个验证函数中正则表达式后面的两个参数分别是正则表达式的旗标和验证失败时显示的错误消息。

安全起见，密码要输入两次。此时要验证两个密码字段中的值是否一致，这种验证可使用WTForms 提供的另一验证函数实现，即 EqualTo。
这个验证函数要附属到两个密码字段中的一个上，另一个字段则作为参数传入。

这个表单还有两个自定义的验证函数，以方法的形式实现。
如果表单类中定义了以validate_ 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用。

本例分别为 email 和 username 字段定义了验证函数，确保填写的值在数据库中没出现过。
自定义的验证函数要想表示验证失败，可以抛出 ValidationError 异常，其参数就是错误消息。

### 8.5.2 注册新用户

处理用户注册的过程没有什么难以理解的地方。提交注册表单，通过验证后，系统就使用用户填写的信息在数据库中添加一个新用户。

app/auth/views.py
```python
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
```

## 8.6 确认账户

对于某些特定类型的程序，有必要确认注册时用户提供的信息是否正确。常见要求是能通过提供的电子邮件地址与用户取得联系。

为验证电子邮件地址，用户注册后，程序会立即发送一封确认邮件。
新账户先被标记成待确认状态，用户按照邮件中的说明操作后，才能证明自己可以被联系上。
账户确认过程中，往往会要求用户点击一个包含确认令牌的特殊 URL 链接。

### 8.6.1 使用itsdangerous生成确认令牌

确认邮件中最简单的确认链接是 http://www.example.com/auth/confirm/<id> 这种形式的URL，其中 id 是数据库分配给用户的数字 id。
但这种实现方式显然不是很安全，只要用户能判断确认链接的格式，就可以随便指定 URL中的数字，从而确认任意账户。

解决方法是把 URL 中的 id 换成将相同信息安全加密后得到的令牌.

itsdangerous 提供了多种生成令牌的方法。
其中，TimedJSONWebSignatureSerializer 类生成具有过期时间的 JSON Web 签名（JSON Web Signatures，JWS）。
这个类的构造函数接收的参数是一个密钥，在 Flask 程序中可使用 SECRET_KEY 设置。

dumps() 方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令牌字符串。
expires_in 参数设置令牌的过期时间，单位为秒.

为了解码令牌，序列化对象提供了 loads() 方法，其唯一的参数是令牌字符串。
这个方法会检验签名和过期时间，如果通过，返回原始数据。
如果提供给 loads() 方法的令牌不正确或过期了，则抛出异常.

将这种生成和检验令牌的功能可添加到 User 模型中.
app/models.py

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db

class User(UserMixin, db.Model):
    # ...
    confirmed = db.Column(db.Boolean, default=False)
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})
        
    def confirm(self, token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
```

generate_confirmation_token() 方法生成一个令牌，有效期默认为一小时。
confirm() 方法检验令牌，如果检验通过，则把新添加的 confirmed 属性设为 True。

### 8.6.2 发送确认邮件

当前的 /register 路由把新用户添加到数据库中后，会重定向到 /index。在重定向之前，这个路由需要发送确认邮件。

app/auth/views.py
```python
from ..email import send_email
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # ...
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
        'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
```

