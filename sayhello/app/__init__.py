# -*- coding: utf-8 -*-
# @Author  : LG

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    db.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app