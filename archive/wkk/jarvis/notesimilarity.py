# -*- coding: utf-8 -*-

import os, sys, codecs, json, re
import jieba
import jieba.analyse
import stopwordsfilter
from math import sqrt
import trainmodel

noteroot = '../Notes/'
testnote = '../Notes/china-and-world.md'
testnote1 = '../Notes/love-barefoot-philosophy.md'
testnote2 = '../Notes/old-wisdom-modern-love.md'
tburl = './seg/tags.txt'
lburl = './data/labelnote.txt'
tagbase = []
matchnotes = []
# this two sentence can solve Chinese Problem
reload(sys)
sys.setdefaultencoding('utf-8')

loglines = []

labeldict = {}

# 类别作为 key，值为笔记列表
def loadlabeldic():
    print 'loading label database'
    labelfile = codecs.open(lburl, 'r', 'utf8')
    for labelline in labelfile:
        arr = labelline[:-len('\n')].split(' ')
        if labeldict.has_key(arr[1]):
            labeldict[arr[1]].append(arr[0])
        else:
            labeldict[arr[1]] = [arr[0]]
    print 'successfully loaded the labels of the notes'
    # printlabeldict()


def printlabeldict():
    for key in labeldict:
        print '[' + key + ']',
        for label in labeldict[key]:
            print label,
        print ''

def loadtagbase():
    tagfile = codecs.open(tburl, 'r')
    for tagline in tagfile:
        tagbase.append(tagline[:-len('\n')].split(' '))

def findsimilarity(note):
    matchnotes = []
    h = codecs.open(note, 'r')
    text = h.read()
    tags = jieba.analyse.extract_tags(text, topK=30)
    loadtagbase()
    ismatch = 0

    tags = stopwordsfilter.stopwordsfilter(tags)

    # start matching
    for tagline in tagbase:
        #tagline is a set of tags for notes
        ismatch = 0
        matchtags = ''
        for tag in tags:
            # tag is one of the tags for testnote
            for mtag in tagline:
                # mtag is one of the tags in one file of the tagbase
                if tag == mtag:
                    # if there is a tag same as the testnote's tag, we add it to the list
                    ismatch = 1
                    matchtags = matchtags + tag + " "
                    break;
        if ismatch == 1:
            matchnotes.append(tagline[0] + " " + matchtags)

    print 'Original Notes'
    print note
    loglines.append('Original Notes: ' + note + '\n')
    print 'Similar Notes:'
    loglines.append('Related Notes:' + '\n')
    for nt in matchnotes:
        loglines.append(nt + '\n')
        print nt
    loglines.append('-------------------')

def checksim(filename,filename2):
    file_words = {}
    ignore_list = [u'的',u'了',u'和',u'呢',u'啊',u'哦',u'恩',u'嗯',u'吧'];
    accepted_chars = re.compile(ur"[\\u4E00-\\u9FA5]+")

    file_object = open(filename)

    try:
        all_the_text = file_object.read()
        seg_list = jieba.cut(all_the_text, cut_all=True)
        #print "/ ".join(seg_list)
        for s in seg_list:
            if accepted_chars.match(s) and s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [1,0]
                else:
                    file_words[s][0] += 1
    finally:
        file_object.close()

    file_object2 = open(filename2)

    try:
        all_the_text = file_object2.read()
        seg_list = jieba.cut(all_the_text, cut_all=True)
        for s in seg_list:
            if accepted_chars.match(s) and s not in ignore_list:
                if s not in file_words.keys():
                    file_words[s] = [0,1]
                else:
                    file_words[s][1] += 1
    finally:
        file_object2.close()

    sum_2 = 0
    sum_file1 = 0
    sum_file2 = 0
    for word in file_words.values():
        sum_2 += word[0]*word[1]
        sum_file1 += word[0]**2
        sum_file2 += word[1]**2

    rate = sum_2/(sqrt(sum_file1*sum_file2+1))
    # print '[',filename,']vs[',filename2,'] rate: ', rate
    return rate

def naivesimallnote():
    noteroot = '../Notes/'
    notes = os.listdir(noteroot)
    count = 0

    for note in notes:
        if note[0] == '.':
            continue
        print 'processing ' + note
        findsimilarity(noteroot + note)

    fh = codecs.open('./result/simnotes.txt', 'w', 'utf-8')
    for line in loglines:
        fh.write(line)

    print 'done'

# 这里这个 note 是包含 name 和 tag 的 list
def kgfindsim(note):
    name = note[0]
    print 'find similar note for', name
    label = trainmodel.noteclassify(note)
    print 'type:',label

    notelist = []

    for content in labeldict[label]:
        notelist.append((content, checksim(noteroot+name, noteroot+content)))

    #L.sort(lambda x,y:cmp(x[1],y[1]))
    notelist.sort(lambda x, y:-cmp(x[1],y[1]))
    print '--------------'
    print 'origin note:', name
    print '--------------'
    print 'similar note:'
    count = 0
    for n in notelist:
        if count < 5:
            print n[0],n[1]
        else:
            break
        count = count + 1

if __name__ == '__main__':
    # checksim(testnote, testnote1)
    loadlabeldic()
    loadtagbase()
    # 随意测试
    note = tagbase[3]
    kgfindsim(note)
