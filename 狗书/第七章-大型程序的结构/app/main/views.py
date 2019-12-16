# -*- coding: utf-8 -*-
# @Author  : LG

from datetime import datetime
from flask import render_template, session, redirect, url_for,flash

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            flash('欢迎新用户!')
            # send_email(to='@.com')
        else:
            session['known'] = True
            flash('欢迎再次使用!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))

    return render_template('index.html',
                           form=form,
                           name = session.get('name'),
                           known = session.get('known'),
                           current_time=datetime.utcnow())

