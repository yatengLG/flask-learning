# -*- coding: utf-8 -*-
# @Author  : LG

from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow(), index=True)

"""
 
"""