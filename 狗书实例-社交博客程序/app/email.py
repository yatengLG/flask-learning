# -*- coding: utf-8 -*-
# @Author  : LG

from app import mail
from flask_mail import Message


def send_email(to, content='邮件内容',title='flask 邮件测试'):
    msg = Message('Flask Test Mail', sender='Flasky Admin <18234835473@163.com>', recipients=[to])
    msg.body = content
    msg.html = '<b>{}</b>'.format(title)
    mail.send(msg)
