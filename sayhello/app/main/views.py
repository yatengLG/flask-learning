# -*- coding: utf-8 -*-
# @Author  : LG

from . import main
from .forms import MessageForm
from ..models import Message
from .. import db
from flask import flash, render_template, redirect, url_for

@main.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        content = form.content.data

        message = Message(name=name, content=content)
        db.session.add(message)
        db.session.commit()

        flash('已提交数据')

        form.name.data = ''
        form.content.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, messages=messages)
