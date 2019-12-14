# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask

# 程序实例是Flask类的对象， 必须创建一个程序实例
app = Flask(__name__)


# 修饰器声明路由，把修饰的函数注册为路由。
# 这里把index()函数注册为程序根地址的处理程序。当浏览器访问根目录时，便会触发 index函数.
@app.route('/')
def index():    # index()这样的函数也被称为视图函数
    # 视图函数的返回值称为响应，是客户端接收到的内容.
    return '<h1> Hello World! <h1>'


# 这里定义的路由中就有一部分是动态名字<name>,尖括号中的内容就是动态部分.
# 调用视图函数时，Flask会将动态部分作为参数传入函数.
# 也支持使用类型定义 如：<int:id>. 支持的类型有：int、float、 path，path 类型也是字符串，但不把斜线视作分隔符
@app.route('/user/<name>')
def user(name):
    return '<h1> Hello {}! <h1>'.format(name)



if __name__ == '__main__':

    # 启动服务器
    app.run(debug=True)