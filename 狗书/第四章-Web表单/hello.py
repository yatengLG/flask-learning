# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

# 每个 Web 表单都由一个继承自 Form 的类，
from flask_wtf import Form
# 文本字段以及提交按钮
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST'])
def index():
    # 在视图中处理表单
    name = None
    form = NameForm()   # 实例化表单
    if form.validate_on_submit():   # 如果数据通过了所有验证，validate_on_submit()返回True
        old_name = session.get('name')
        if form.name.data != old_name:
            flash('Looks like you have changed your name!')
        session['name']=form.name.data
        return redirect(url_for('index'))
    # render_template函数的第一个参数是模板的文件名
    return render_template('index.html', form=form, name=session.get('name'))
"""
代码解释：
当用户第一次访问时，服务器收到一个get请求，validate_on_submit返回False, 直接返回index.html，
form通过模板渲染为表单，其中name=None，通过模板进行判断显示；
当用户提交表单后，经验证 如果名字不为空，则validate_on_submit返回True, 从表单中获取name值，并将表单中name置为空。"""

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