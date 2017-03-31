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

