#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    GUITARPA_MAIL_SUBJECT_PREFIX = '[Guitarpa]'
    GUITARPA_MAIL_SENDER = 'conan582905668 <conan582905668@qq.com>'
    GUITARPA_ADMIN = os.environ.get('GUITARPA_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 这个是pycharm建议加的，说是这项配置在未来的版本中会被默认为禁止状态，把它设置为True即可取消warning

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# 把错误通过邮件发给管理员

@classmethod
def init_app(cls, app):
    Config.init_app(app)

    # email errors to the administrators
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None
    if getattr(cls, 'MAIL_USERNAME', None) is not None:
        credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        if getattr(cls, 'MAIL_USE_TLS', None):
            secure = ()
    mail_handler = SMTPHandler(
        mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        fromaddr=cls.GUITARPA_MAIL_SENDER,
        toaddrs=[cls.GUITARPA_ADMIN],
        subject=cls.GUITARPA_MAIL_SUBJECT_PREFIX + ' Application Error',
        credentials=credentials,
        secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}