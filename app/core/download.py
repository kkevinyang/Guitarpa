# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, urllib
import re
from reportlab.pdfgen import canvas
import os
from ..loggers  import orilogger
from flask import Response

# 此文件已不用
# 此文件已不用
# 此文件已不用
# 此文件已不用
# 此文件已不用
# 此文件已不用



class Download:
    def __init__(self,id):
        self.id = id
        self.for_url()
        self.for_pdf()
        #self.res()


    def for_url(self):
        try:
            #获取html
            page_url = 'http://www.yuesir.com/ipu/' + str(self.id) + '.html'
            request = urllib2.Request(page_url)
            response = urllib2.urlopen(request)
            html = response.read()
            #with urllib.request.urlopen(page_url) as url:
            #    html = url.read()

            # 获取标题
            bs = BeautifulSoup(html,"html.parser")
            self.title=bs.find("h2").string.split(' ')[0]# 把后面难看的‘吉他谱’三个字去掉
            print self.title
            # 获取url
            pattern = re.compile('<img class="page-post-main-content-list-item-img" src="(.*?)".*?')
            self.pic_urls = re.findall(pattern,html)
        except:
            orilogger.exception(u'生成html失败!')


    def for_pdf(self):
        try:
            filename = self.title+".pdf"
            c = canvas.Canvas(u"app/data/" + self.title+u".pdf")
            i = 1
            for pic_url in self.pic_urls:
                # 写入图片
                u = urllib.urlopen(pic_url)
                data = u.read()
                name = self.title + str(i)
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
            response = Response(c)
            response.headers["Content-Disposition"] = "attachment; filename='laonanha.pdf'"
            response.headers["Content-Type"] = "application/pdf"

            return response


        except:
            orilogger.exception(u'导入pdf失败!')


