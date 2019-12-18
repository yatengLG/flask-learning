# -*- coding: utf-8 -*-
# @Author  : LG

from sayhello.app import db
from datetime import datetime

class Message(db.Model):
    # 设置id为主键
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    content = db.Column(db.String(200))

    # index = True 为这列创建索引，提升查询效率
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
