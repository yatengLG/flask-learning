# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

main = Blueprint('main', __name__)

from . import errors, views

