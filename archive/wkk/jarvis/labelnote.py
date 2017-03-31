#coding=utf-8
import os, sys, codecs, json, re

noteroot = '../Notes'

types = [u'技术',u'地理',u'总类',u'科学',u'历史',u'社会',u'人物',u'社会科学',u'宗教',u'文化',u'休闲',u'生活',u'自然',u'科技',u'自然科学']

content = []

def labelnote():
    files = os.listdir(noteroot)

    for f in files:
        if f[0] == '.': continue
        printtypes()
        print '[', f , ']'
        index = int(raw_input("input the type of the note:\n"))
        temp = f + ' ' + types[index-1] + '\n'
        print 'Tagged: [',
        print f,']',
        print types[index-1]
        content.append(temp)

    fh = codecs.open('./data/labelnote.txt', 'w', 'utf-8')
    for c in content:
        fh.write(c)
    print '写入完成'


def printtypes():
    index = 1
    for t in types:
        print str(index), ' ', t
        index = index + 1



if __name__ == '__main__':
    labelnote()
