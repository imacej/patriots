#coding=utf-8
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Entity:
    '表示实体的类'

    def __init__(self, name, parent, child):
        self.name = name
        self.parent = parent
        self.child = child
        self.sample = []

    def displayEntity(self):
        print "-----Entity [",
        for n in self.name:
            print n,
        print "]-----"
        print "Parent:",
        for p in self.parent:
            print p,
        print ''
        print "Child:",
        for c in self.child:
            print c,
        print ''
        print "Sample:",
        for s in self.sample:
            print s,
        print ''

class Record:
    '每条日志的类'

    def __init__(self, intime, pid, bid, docid, ip, query):
        self.intime = intime
        self.pid = pid
        self.bid = bid
        self.docid = docid
        self.ip = ip 
        self.query = query
        self.province = "" 
        self.city = ""
        self.doctype = "" # 根据 docid 获取的类别
        self.doctext = "" # 根据 docid 获取的 faq 文本
        self.words = [] # 分词后的 query
        self.keywords = [] # 提取出的关键词
        self.knodes = [] # 属于知识图谱节点
        self.sentiment = 0.0 # 情感值

    def displayRecord(self):
        print "-----Record [", self.query, "]-----"
        print "类型:", self.doctype
        print "位置:", self.province, self.city
        print "情感:", self.sentiment
        print "分词:",
        for w in self.words:
            print w.encode('utf-8'),
        print ''
        print '关键词:',
        for w in self.keywords:
            print w.encode('utf-8'),
        print ''
        print '知识图谱节点:',
        for w in self.knodes:
            print w.encode('utf-8'),
        print ''


def obj2dict(obj):
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d

def dict2obj(self, d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items())
        instance = class_(**args)
    else:
        instance = d
    return instance
