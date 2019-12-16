# 第六章 电子邮件

很多类型的应用程序都需要在特定事件发生时提醒用户，而常用的通信方法是电子邮件。
虽然 Python 标准库中的 smtplib 包可用在 Flask 程序中发送电子邮件，
但包装了 smtplib 的Flask-Mail 扩展能更好地和 Flask 集成。

# 使用Flask-Mail提供电子邮件支持

安装: ``` pip install flask-mail```

Flask-Mail 连接到简单邮件传输协议（Simple Mail Transfer Protocol，SMTP）服务器，并把邮件交给这个服务器发送。

如果不进行配置，Flask-Mail 会连接 localhost 上的端口 25，无需验证即可发送电子邮件。

Flask-Mail SMTP服务器的配置：

|配置|默认值|说明|
|:----:|:----:|:----:|
|MAIL_SERVER    |localhost  |电子邮件服务器的主机名或 IP 地址|
|MAIL_PORT      |25         |电子邮件服务器的端口|
|MAIL_USE_TLS   |False      |启用传输层安全（Transport Layer Security，TLS）协议|
|MAIL_USE_SSL   |False      |启用安全套接层（Secure Sockets Layer，SSL）协议|
|MAIL_USERNAME  |None       |邮件账户的用户名|
|MAIL_PASSWORD  |None       |邮件账户的密码|

示例，展示了如何配置程序，以便使用 Google Gmail 账户发送电子邮件。
```python
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```

Flask-Mail 的初始化方法如示例：
```python
from flask.ext.mail import Mail
mail = Mail(app)
```

这部分更新较少，只在hello.py中做出部分修改。
在hello.py中配置好邮件设置，在新用户登录后，即会发送一个邮件。
详情见hello.py