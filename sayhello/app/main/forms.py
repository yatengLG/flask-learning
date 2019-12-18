# -*- coding: utf-8 -*-
# @Author  : LG

from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, DataRequired, Length

class MessageForm(Form):
    name = StringField('Name', validators=[Required(), DataRequired(), Length(1, 20)])
    content = TextAreaField('Message', validators=[Required(), DataRequired(), Length(1, 200)])
    submit = SubmitField('Submit')
