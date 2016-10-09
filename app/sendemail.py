#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
#from app import create_app
from . import mail
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#@celery.task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

    #return {'status': 'Send task done!'}


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['GUITARPA_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['GUITARPA_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def sendto_kindle(to,name):

    app = current_app._get_current_object()
    msg = Message(app.config['GUITARPA_MAIL_SUBJECT_PREFIX'] + ' ' + u'Your PDF coming!',
                  sender=app.config['GUITARPA_MAIL_SENDER'], recipients=[to])
    msg.body = u"Guitarpa"
    msg.html = u"<b>Guitarpa provide this service for you!</b>"
    with app.open_resource(u"core/" + name + u'.pdf') as po:
        msg.attach(u'Guitarpa.pdf', "*/*", po.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    # 异步开启
    thr.start()
    return thr

