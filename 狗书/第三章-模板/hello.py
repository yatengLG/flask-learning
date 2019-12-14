# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    # render_template函数的第一个参数是模板的文件名
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    # render_template函数的第一个参数是模板的文件名，随后的参数是键对值。
    return render_template('user.html',name=name)

# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)