# -*- coding: utf-8 -*-
# @Author  : LG

from . import main
from flask import render_template

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

