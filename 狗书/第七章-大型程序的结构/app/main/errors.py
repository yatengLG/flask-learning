# -*- coding: utf-8 -*-
# @Author  : LG

from flask import render_template
from . import main

# 要想注册程序全局的错误处理程序，必须使用 app_errorhandler
# 使用 errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_errro(e):
    return render_template('505.html'), 500

