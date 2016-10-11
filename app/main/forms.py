#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email
from ..models import User


class SearchForm(FlaskForm):
    keyword = StringField(u'请输入吉他曲名称或关键字查询：', validators=[DataRequired()])
    submit = SubmitField(u'搜索')

class EditProfileForm(FlaskForm):
    send_loc = StringField(u'推送邮箱：', validators=[Length(0, 64),Email()])

    submit = SubmitField(u'保存')

class MessageForm(FlaskForm):
    message = TextAreaField(u'内容', validators=[DataRequired()])
    submit = SubmitField(u'留言')