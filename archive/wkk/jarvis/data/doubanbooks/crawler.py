#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import codecs
import collections
import urllib2, sys
import logging
import random

from bs4 import BeautifulSoup

logger = logging.getLogger('Crawler')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('crawler.log')
fh.setLevel(logging.DEBUG) 
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class Tag(object):
    
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.start = 0
        self.books = []
        self.maxstart = None
        self.firstTime = True
        self.finished = False


class Boook(object):
    def __init__(self, doubanid, name, context, tags):
        self.doubanid = doubanid
        self.name = name
        self.context = context
        self.tags = tags

class TagsKeeper(object):
    
    topTagsName = [
                   u'科普', u'互联网', u'编程', u'科学' u'交互设计 ', u'用户体验', u'算法',
                   u'爱情', u'旅行', u'生活', u'励志', u'摄影', u'成长', u'心理', u'职场',
                   u'女性', u'游记', u'美食', u'教育', u'灵修', u'情感 ', u'健康', u'手工',
                   u'养生', u'两性', u'家居', u'人际关系', u'自助游'
                  ]
    
    
    topTagsL = []
    topTagsD = dict()
        
    for i in topTagsName:
        t = Tag(i)
        topTagsL += [t]
        topTagsD[i] = t
        
    otherTagsL = []
    otherTagsD = dict()
    
    i = 0

    @classmethod
    def TagGen2Crawl(cls):
        logger.debug("len of other tag list %d %d" % (len(cls.otherTagsL), cls.i))
        if cls.i % 3 != 0 and len(cls.otherTagsL) != 0:
            logger.debug("Get the tag from other tag list.")
            cls.i += 1
            return random.choice(cls.otherTagsL)
        else:
            logger.debug("Get the tag from top tag list.")
            cls.i += 1
            return random.choice(cls.topTagsL)
        
        
            
    @classmethod
    def AddTag(cls, name):
        if name not in cls.otherTagsD and name not in cls.topTagsD:
            t = Tag(name)
            cls.otherTagsL += [t]
            cls.otherTagsD[name] = t
            
    @classmethod
    def TagBookP1(cls, name, doubanid):
        if name in cls.otherTagsD:
            cls.otherTagsD[name].count += 1
            cls.otherTagsD[name].books += [doubanid]
        if name in cls.topTagsD:
            cls.topTagsD[name].books += [doubanid]
    
    @classmethod
    def TagName2Url(cls, name, start=0):
        url = ur"http://book.douban.com/tag/" + name \
        +ur"?start=" + unicode(start)+ur"&type=T"
        return urllib2.unquote(url)
        
        

class BooksKeeper(object):
    booknum = 0
    books = dict()
    
    fobj = open("doubanbooks.dat", "w")
    @classmethod
    def AddBook(cls, book):
        if book.doubanid not in cls.books:
            cls.books[book.doubanid] = book
            s = json.dumps({u'id': book.doubanid, u'name':book.name
                        ,u'context':book.context, u'tags':book.tags}, ensure_ascii=False, encoding="utf-8")
            print >> cls.fobj, s
            cls.fobj.flush()
            logger.debug("Record a book.")
            logger.debug("-"*20)
            
            cls.booknum += 1
            logger.debug(cls.booknum)
        

class Crawler(object):
    
    pagesforcraw = []
    
    @classmethod
    def CrawlerTagPage(cls, tag):
        logger.debug("Crawl tag %s." % tag.name)
	try:
		if tag.finished == True:
		    return
		
		url = TagsKeeper.TagName2Url(tag.name, tag.start)
		tag.start += 20
	      
		opener = urllib2.build_opener()
		req = urllib2.Request(url)
		html = opener.open(req).read()
		soup = BeautifulSoup(html)
		
		booklinks = []
		booknames = []
		
		subs = soup.find("ul", {'class':'subject-list'}).findAll('li', {'class':'subject-item'})

		
		for i in subs:
		    a = i.find('div',{'class':'info'}).find('a')
		    booklinks += [a.get('href')]
		    booknames += [a.get('title')]
		
		logger.debug("Get %d books from tag this page." % len(booklinks))
		
		if tag.firstTime == True:
		    starts = []
		    pat = re.compile(ur'start=\d+&type=T')
		    patstart = ur'start=(\d+)'
		    paginator = soup.find('div', {'class':'paginator'}).findAll('a', {'href':pat})

		    for i in paginator:
			starts += [re.search(r'start=(\d+)', i.get('href')).groups()[0]]

		    starts = map(lambda x: int(x), starts)
		    tag.maxstart = max(starts)
		    logger.debug("Get maxstart %d." % tag.maxstart)
		
		tag.firstTime = False
		if tag.start == tag.maxstart:
		    tag.finished == True
		    
		cls.pagesforcraw = booklinks
	except:
		return
        
        
    @classmethod
    def CrawlerBookPage(cls, url):
        logger.debug("Crawl book page: %s" % url)

	try:
		doubanid = int(re.search(ur'http://book.douban.com/subject/(\d+)/', url).groups()[0])
		opener = urllib2.build_opener()
		req = urllib2.Request(url)
		html = opener.open(req).read()
		soup = BeautifulSoup(html)
		
		ctp = soup.find('div',{'class':'related_info'}).findAll('div', {'class':"intro"})
		context = "".join([i.text for i in ctp[-1].findAll('p')])
		
		tlc = soup.find('div',{'id':'db-tags-section'}).find('div', {'class':'indent'})
		lnt = tlc.findAll('a')
		
		pat = re.compile(ur"\(\d+\)")
		reret = re.findall(pat, tlc.text)

		taglinks = [i.get('href') for i in lnt]
		tagnames = [i.text for i in lnt ]
		tagcnts =  [int(i[1:-1]) for i in reret ]
		
		name = soup.find('h1').span.text
		logger.debug("Book context %s." % context)
		b = Boook(doubanid, name, context, zip(tagnames, tagcnts))
		BooksKeeper.AddBook(b)
		for i in tagnames:
		    logger.debug("Add tag %s." % i)
		    TagsKeeper.AddTag(i)
		    TagsKeeper.TagBookP1(i, doubanid)
	except:
		return
        
    @classmethod
    def run(cls, num):
        
        
        logger.debug("Crawler run...")
        
        while True:
            logger.debug(BooksKeeper.booknum)
            tag = TagsKeeper.TagGen2Crawl()
            logger.debug("Crawl tag: %s" % tag.name)
            cls.CrawlerTagPage(tag)
            for l in cls.pagesforcraw:
                cls.CrawlerBookPage(l)
                if BooksKeeper.booknum >= num:
                    exit()
        
        
        
        
    

if __name__ == "__main__":
    Crawler.run(10000)
