# -*- coding: utf-8 -*-

class BookInfo:
    def __init__(self):
        self._title = ''
        self._subtitle = ''
        self._author = ''
        self._translator = ''
        self._series = ''
        self._publisher = ''
        self._publishyear = ''
        self._pages = ''
        self._price = ''
        self._version = ''
        self._ISBN = ''
        self._originname = ''
        self._score = ''
        self._count = '' # 评价人数
        self._5star = '' # 百分比
        self._4star = ''
        self._3star = ''
        self._2star = ''
        self._1star = ''
        self._introcontent = ''
        self._introauthor = ''
        self._tags = []
        # 0表示第一部分 基本信息
        # 1表示第二部分 评分
        # 2表示第三部分 内容简介
        # 3表示第四部分 作者简介
        # 4表示第五部分 目录
        # 5表示第六部分 标签
        self._flag = 0
        self._linegap = 4

    def __str__(self):
        print("BookInfo(%s,%s,%s)" % (self._title, self._author, self._score))

    def description(self):
        if self._title != '':
            print '书名: ' + self._title
        if self._subtitle != '':
            print '副标题: ' + self._subtitle
        if self._author != '':
            print '作者: ' + self._author
        if self._translator != '':
            print '译者: ' + self._translator
        if self._series != '':
            print '系列: ' + self._series
        if self._publisher != '':
            print '出版社: ' + self._publisher
        if self._publishyear != '':
            print '出版年: ' + self._publishyear
        if self._pages != '':
            print '页数: ' + self._pages
        if self._price != '':
            print '价格: ' + self._price
        if self._version != '':
            print '装帧: ' + self._version
        if self._ISBN != '':
            print 'ISBN: ' + self._ISBN
        if self._originname != '':
            print '原名: ' + self._originname
        if self._score != '':
            print '评分: ' + self._score
        if self._count != '':
            print '人数: ' + self._count
        if self._5star != '':
            print '五星: ' + self._5star
        if self._4star != '':
            print '四星: ' + self._4star
        if self._3star != '':
            print '三星: ' + self._3star
        if self._2star != '':
            print '二星: ' + self._2star
        if self._1star != '':
            print '一星: ' + self._1star
        if self._introcontent != '':
            print '内容介绍: ' + self._introcontent
        if self._introauthor != '':
            print '作者介绍: ' + self._introauthor
        print '标签: ',
        for tag in self._tags:
            print tag,
        print '\ndone'

    def output(self):
        # 选取一些有效的数据进行输出
        data = ''


    def addinfo(self, line):
        if self._flag == 0:
            #print line[:6]
            if line[:6] == '书名':
                self._title = line[7:]
            elif line[:6] == '作者':
                self._author = line[7:]
            elif line[:6] == '译者':
                self._translator = line[7:]
            elif line[:6] == '丛书':
                self._series = line[7:]
            elif line[:9] == '出版社':
                self._publisher = line[10:]
            elif line[:9] == '出版年':
                self._publishyear = line[10:]
            elif line[:6] == '页数':
                self._pages = line[7:]
            elif line[:6] == '定价':
                self._price = line[7:]
            elif line[:6] == '装帧':
                self._version = line[7:]
            elif line[:4] == 'ISBN':
                self._ISBN = line[5:]
            elif line[:9] == '副标题':
                self._translator = line[10:]
            elif line[:9] == '原作名':
                self._translator = line[10:]
            else:
                self._flag = 1
        elif self._flag == 1:
            if line[:6] == '得分':
                self._score = line[7:]
            elif line[:12] == '评价人数':
                self._count = line[13:]
            elif line[:12] == '力荐比例':
                self._5star = line[13:]
            elif line[:12] == '推荐比例':
                self._4star = line[13:]
            elif line[:12] == '还行比例':
                self._3star = line[13:]
            elif line[:12] == '较差比例':
                self._2star = line[13:]
            elif line[:12] == '很差比例':
                self._1star = line[13:]
            else:
                self._flag = 2
        elif self._flag == 2:
            if line[:12] == '内容简介':
                self._introcontent = line[13:]
            elif len(line) > self._linegap:
                self._introcontent = self._introcontent + line
            else:
                self._flag = 3
        elif self._flag == 3:
            if line[:12] == '作者简介':
                self._introauthor = line[13:]
            elif len(line) > self._linegap:
                self._introauthor = self._introauthor + line
            else:
                self._flag = 4
        elif self._flag == 4:
            if len(line) > self._linegap:
                pass
            else:
                self._flag = 5
        elif self._flag == 5:
            if line[:6] == '标签':
                pass
            elif len(line) > self._linegap:
                self._tags.append(line)
            else:
                self._flag = 6
        else:
            pass
