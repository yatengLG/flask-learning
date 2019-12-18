# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views