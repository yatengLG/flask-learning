# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MessageForm(Form):
    name = StringField('name',validators=[DataRequired(), Length(1, 20)])
    content = TextAreaField('content', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()
