# -*- coding: utf-8 -*-
# @Author  : LG

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardstrings'

