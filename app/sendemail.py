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

from bs4 import BeautifulSoup
import urllib2, urllib
import re
from reportlab.pdfgen import canvas
import os


import sys
reload(sys)
sys.setdefaultencoding('utf8')

from core import USER_AGENTS
import random

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

    app = current_app._get_current_object()
    msg = Message(app.config['GUITARPA_MAIL_SUBJECT_PREFIX'] + ' ' + u'Your PDF coming!',
                  sender=app.config['GUITARPA_MAIL_SENDER'], recipients=[to])
    msg.body = u"Guitarpa"
    msg.html = u"<b>Guitarpa provide this service for you!</b>"
    # 下面先下载ｐｄｆ
    #获取html
    page_url = 'http://www.yuesir.com/ipu/' + str(id) + '.html'
    user_agent = random.choice(USER_AGENTS)
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(page_url, None, headers)
    response = urllib2.urlopen(request)
    html = response.read()
    # 获取标题
    bs = BeautifulSoup(html,"html.parser")
    title=bs.find("h2").string.split(' ')[0]# 把后面难看的‘吉他谱’三个字去掉
    print title
    # 获取url
    pattern = re.compile('<img class="page-post-main-content-list-item-img" src="(.*?)".*?')
    pic_urls = re.findall(pattern,html)
    #filename = title+".pdf"
    only_name = title.encode('utf-8')+u".pdf"
    filename = u"app/data/" + title+u".pdf"

    c = canvas.Canvas(filename)
    i = 1
    for pic_url in pic_urls:
        # 写入图片
        u = urllib.urlopen(pic_url)
        data = u.read()
        name = title + str(i)
        f = open(name, 'wb')
        f.write(data)
        f.close()
        i = i+1
        #写入pdf
        dim=c.drawImage(name,0,0)
        c.setPageSize(dim)
        c.showPage()
        #删除原gif
        os.remove(name)
    c.save()
    print filename
    print callable(filename)
    # 尝试返回响应
    raw_bytes = ""
    with open(filename, 'rb') as r:
        #msg.attach('Guitarpa_pdf', "*/*", r.read())
        msg.attach('Guitarpa_pdf', "*/*", r.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    '''
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "attachment; filename=" + only_name.encode('utf-8')
    return response
    '''

