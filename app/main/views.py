#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, Response,make_response
from . import main
from .forms import EditProfileForm,SearchForm,MessageForm
from ..core import Search, Download
from flask_login import login_required, current_user,AnonymousUserMixin
from .. import db
from ..models import Message
from ..sendemail import sendto_kindle
#from .. import app

from bs4 import BeautifulSoup
import urllib2, urllib
import re
from reportlab.pdfgen import canvas
import os
from ..loggers  import orilogger
from flask import Response
import sys
reload(sys)
sys.setdefaultencoding('utf8')

@main.route('/',methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data #keyword是自定义的传递名字的变量
        return redirect(url_for('.search_res',keyword=keyword))
    return render_template('index.html',form=form)

@main.route('/search_res/<keyword>',methods=['GET', 'POST'])
def search_res(keyword):
    if keyword != None:
        res_list = Search(keyword).res_list # core模块的search.py
        if res_list == [] or res_list[0].name == '《爱情》':
            flash(u'未找到相关的曲谱，请输入恰当的关键词！')
        return render_template('search_res.html',result = res_list)
    else:
        flash('请输入关键词！')
        return redirect(url_for('.index'))
'''
@main.route('/download/<id>')
def download(id):
    try:
        flash(id)
        Download(id)
        return render_template('index.html',response=response)
    except:
        return redirect(url_for('main.edit_profile'))
'''
@main.route('/download/<id>')
def download(id):
    #try:
    #获取html
    page_url = 'http://www.yuesir.com/ipu/' + str(id) + '.html'
    request = urllib2.Request(page_url)
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
    only_name = title+u".pdf"
    filename = u"app/data/" + title+u".pdf"
    print type(filename)
    print filename

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
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "attachment; filename=" + only_name.encode('utf-8')
    return response

    '''
        a = open(filename)
    print callable(a)
    #with open(filename,'r') as t:
      #  return t
        #return t.read().decode('utf-8')
    #print callable(t)

    #content = open(filename.read(), 'rb')#, 'utf-8')
    response = make_response(t)
    response.headers["Content-Disposition"] = "attachment; filename="+filename.encode('utf-8')
    response.headers["Content-Type"] = "application/pdf"
    flash(id)

    return response
    content.close()
    #Download(id)
    #return render_template('index.html',response=response)
   # except:
       # return render_template('try.html',filename=filename)
        #return redirect(url_for('main.edit_profile'))

    #a = open(filename)
    print callable(a)
    #with open(filename,'r') as t:
      #  return t
        #return t.read().decode('utf-8')
    #print callable(t)

    #content = open(filename.read(), 'rb')#, 'utf-8')
    response = make_response(t)
    response.headers["Content-Disposition"] = "attachment; filename="+filename.encode('utf-8')
    response.headers["Content-Type"] = "application/pdf"
    flash(id)

    return response
    content.close()
    #Download(id)
    #return render_template('index.html',response=response)
   # except:
       # return render_template('try.html',filename=filename)
        #return redirect(url_for('main.edit_profile'))
'''




'''
@main.route('/download/<author>/<name>/<item_url>')
@login_required

def download():
    #if current_user.kindle_loc == None:
       # flash(u'请先填写你的邮箱!')
    #else:
        #hardtask.delay(current_user.kindle_loc,origin,bookid,bookname)
        #Down(item_url)
        #sendto_kindle(current_user.kindle_loc, name=name)
        #flash(u'你的推送已加入任务队列，请注意查收。')
    #return redirect(url_for('.index'))
        return render_template('try.html')



@main.route('/download/<id>')
def download(id):

    try:
        flash(id)
        Download(id)
    except:
        return redirect(url_for('.index'))
    #res()
    #return response
    #return render_template('download.html',qu_id = id)

@main.route('/download_result/<id>')
def download_result(id):
    flash(id)
    with app.open_resource(u"core/" + name + u'.pdf') as po:
        content = po
    response = Response(content)
    #response = make_response(content)
    flash('get')
    response.headers["Content-Disposition"] = "attachment; filename=筷子兄弟《老男孩》.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response
    #return render_template('download.html')
'''

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.kindle_loc = form.kindle_loc.data

        db.session.add(current_user)
        db.session.commit()
        flash(u'你的信息已更新.')
        return redirect(url_for('.index'))
    form.kindle_loc.data = current_user.kindle_loc
    return render_template('edit_profile.html', form=form)

@main.route('/letschat',methods = ['GET','POST'])
def letschat():
    form = MessageForm()
    messages = Message.query.order_by(Message.time.desc()).all()
    if form.validate_on_submit():
        if current_user.id == -1:
            flash(u'请登录后留言。')
            return redirect(url_for('.letschat'))
        message = Message(user_name=current_user.username,user_id=current_user.id,\
                          message = form.message.data)

        db.session.add(message)
        db.session.commit()
        return redirect(url_for('.letschat'))
    return render_template('letschat.html',messages = messages,form = form)