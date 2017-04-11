#coding=utf-8

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

    def displayRecord(self):
        print "-----Record [", self.query, "]-----"
        print "类型:", self.doctype
        print "位置:", self.province, self.city
        print "分词:",
        for w in self.words:
            print w,
        print ''

