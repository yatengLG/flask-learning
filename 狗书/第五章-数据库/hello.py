# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

# 每个 Web 表单都由一个继承自 Form 的类，
from flask_wtf import Form
# 文本字段以及提交按钮
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_sqlalchemy import SQLAlchemy

# 表单类
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
bootstrap = Bootstrap(app)

# 表单使用
app.config['SECRET_KEY'] = 'hard to guess string'

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
# 数据库模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

# 数据库模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# 数据库创建表
db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    # 在视图中处理表单
    form = NameForm()   # 实例化表单
    if form.validate_on_submit():   # 如果数据通过了所有验证，validate_on_submit()返回True
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            flash('欢迎新用户!')

        else:
            session['known'] = True
            flash('欢迎旧用户!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name = session.get('name'),
                           known = session.get('known', False)
                           )
"""
代码解释：
当用户第一次访问时，服务器收到一个get请求，validate_on_submit返回False, 直接返回index.html，
form通过模板渲染为表单，其中name=None，通过模板进行判断显示；
当用户提交表单后，在数据库中进行查询，如果数据库中存在，则 将会话中known写为True。 更新会话，重定向到首页。
如果数据库中不存在，则新建一条数据，提交到数据库，并将会话中known写为False. 更新会话，重定向到首页.
"""

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