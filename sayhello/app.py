# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask
from main import main as main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)


# from sayhello import views

app.run()