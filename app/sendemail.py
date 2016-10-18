#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from .core import Download
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)



def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['GUITARPA_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['GUITARPA_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_loc_email(to,id):
    # 邮件初始设置
    filename = Download(id).for_pdf()

    app = current_app._get_current_object()
    msg = Message(app.config['GUITARPA_MAIL_SUBJECT_PREFIX'] + ' ' + u'Your PDF coming!',
                  sender=app.config['GUITARPA_MAIL_SENDER'], recipients=[to])
    msg.body = u"Guitarpa"
    msg.html = u"<b>Guitarpa provide this service for you!</b>"
    with open(filename, 'rb') as r:
        msg.attach('Guitarpa_pdf', "*/*", r.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

