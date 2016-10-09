#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Qupu:
    name = ''
    author = ''
    id = ''
    item_url = ''

class Search:
    def __init__(self,keyword):
        self.keyword = keyword
        #self.res_list = []
        self.search_aiyuepu()

    def search_aiyuepu(self):
        self.res_list = []
        _searchurl = 'http://www.yuesir.com/ipu/search.php?kw=' + self.keyword
        the_res = []
        #qupu = Qupu()
        #获取html
        request = urllib2.Request(_searchurl)
        response = urllib2.urlopen(request)
        page = response.read()
        #　用正则匹配结果的信息
        pattern = re.compile('<li>\s* <a class="title" title="(.*?)" href="(.*?).html.*?</a>.*?<div class="url">(.*?)</div>',re.S)
        #pattern = re.compile('<li>\s* <a class="title" title="(.*?)" href=.*?</a>.*?<div class="url">(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            #title = item[0]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          = item[0]
            qupu = Qupu()
            qupu.name = item[0].split(' - ')[0]
            qupu.author = item[0].split(' - ')[1]
            qupu.id = item[1]
            qupu.item_url = item[2]
            the_res.append(qupu)
        self.res_list=the_res # 把获得的结果赋予到类的属性上，更方便之后调用
        return the_res

        if the_res == []:
            flash(u'未找到包含关键字\"' + self.keyword + u'\"的曲谱')
            return the_res