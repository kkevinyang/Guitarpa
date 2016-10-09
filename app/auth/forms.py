# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'自动登录')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(3, 64)])
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次密码须一致。')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次密码须一致。')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'重置密码')


class PasswordResetForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码须一致。')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知邮箱地址.')


class ChangeEmailForm(FlaskForm):
    email = StringField(u'新邮箱', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'更新邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册.')
