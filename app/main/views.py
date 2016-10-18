#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, flash, make_response
from . import main
from .forms import EditProfileForm,SearchForm,MessageForm
from ..core import Search, Download
from flask_login import login_required, current_user,AnonymousUserMixin
from .. import db
from ..models import Message
from ..sendemail import send_loc_email

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

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

@main.route('/send/<id>')
@login_required
def send(id):
    if current_user.send_loc == None:
        flash(u'请先填写你要接受推送的邮箱')
        return redirect(url_for('main.edit_profile'))
    else:
        send_loc_email(current_user.send_loc,id)
        flash(u'你的推送已加入任务队列，请注意查收。')
    return redirect(url_for('.index'))



@main.route('/download/<id>')
def download(id):
    filename = Download(id).for_pdf()
    raw_bytes = ""
    with open(filename, 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "attachment; filename=" + filename.split('/')[2].encode('utf-8')#only_name.encode('utf-8')
    return response



@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.send_loc = form.send_loc.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'你的信息已更新.')
        return redirect(url_for('.index'))
    form.send_loc.data = current_user.send_loc
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

@main.route('/about',methods = ['GET','POST'])
def about():
    return render_template('about.html')