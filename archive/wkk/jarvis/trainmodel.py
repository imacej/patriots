#coding=utf-8
import os, sys, codecs, json, re

# train model for the specific count

'''
生成倒排索引的流程：
笔记 -> label -> tag -> 倒排索引 -> 给每个 tag 标记好所属的 label(即为类别)

预测时的流程
笔记 -> tag -> 倒排索引 -> 统计不同 label 的次数 -> 做出预测

'''

traindata = []
testdata = []
noteroot = '../Notes'
tburl = './seg/tags.txt'
lburl = './data/labelnote.txt'
labeldict = {}
invindex = {}

types = [u'技术',u'地理',u'总类',u'科学',u'历史',u'社会',u'人物',u'社会科学',u'宗教',u'文化',u'休闲',u'生活',u'自然',u'科技',u'自然科学']

trainsetsize = 100
modelsize = 200


def splitdata(count):
    print 'spliting data for training'
    tagfile = codecs.open(tburl, 'r', 'utf8')
    num = 0
    for tagline in tagfile:
        if num < count:
            traindata.append(tagline[:-len('\n')].split(' '))
        else:
            testdata.append(tagline[:-len('\n')].split(' '))
        num = num + 1
    print 'successfully split ', count, ' notes as training data'

# load all the tagged file, store in a dictionary
def loadlabel():
    print 'loading label database'
    labelfile = codecs.open(lburl, 'r', 'utf8')
    for labelline in labelfile:
        arr = labelline[:-len('\n')].split(' ')
        labeldict[arr[0]] = arr[1]
    print 'successfully loaded the labels of the notes'

def buildinvertedindex():
    print 'building inverted index'
    for record in traindata:
        name = record[0]
        label = labeldict[name]
        print name, label
        for tag in record:
            if tag == name:
                continue
            if invindex.has_key(tag):
                invindex[tag].append(label)
            else:
                invindex[tag] = [label]
    print 'successfully build inverted index'

def printinvdict():
    for key in invindex:
        print '[' + key + ']',
        for label in invindex[key]:
            print label,
        print ''

def saveinvdict():
    print 'save inverted index'
    output = ''
    for key in invindex:
        output = output + key
        print '[' + key + ']',
        for label in invindex[key]:
            output = output + ' ' + label
            print label,
        output = output + '\n'
        print ''
    fh = codecs.open('./data/invnotes.txt', 'w', 'utf-8')
    fh.write(output)
    print 'successfully save to file'

def testresult():
    print 'testing note classification'
    print '---------------------------'
    print 'test size:', len(testdata)

    correct = 0

    for record in testdata:
        correct = correct + testnoteclassify(record)

    print 'precision rate:', correct,'/',len(testdata)


def noteclassify(note):
    splitdata(modelsize)
    loadlabel()
    # build inverted index with dictionary and list
    buildinvertedindex()
    name = note[0]
    print 'name:', name
    typedic = {}
    for tag in note:
        if tag == name:
            continue
        if invindex.has_key(tag):
            label = invindex[tag]
            for t in label:
                if typedic.has_key(t):
                    typedic[t] = typedic[t] + 1
                else:
                    typedic[t] = 1
    # correct label
    truelabel = labeldict[name]
    # predict label
    prelabel = ''
    precount = 0
    for key in typedic:
        if typedic[key] > precount:
            precount = typedic[key]
            prelabel = key

    return prelabel

def testnoteclassify(note):
    name = note[0]
    print 'name:', name
    typedic = {}
    for tag in note:
        if tag == name:
            continue
        if invindex.has_key(tag):
            label = invindex[tag]
            for t in label:
                if typedic.has_key(t):
                    typedic[t] = typedic[t] + 1
                else:
                    typedic[t] = 1
    '''
    for key in typedic:
        print '[' + key + ']',
        print typedic[key],
        print ''

    '''
    # correct label
    truelabel = labeldict[name]
    # predict label
    prelabel = ''
    precount = 0
    for key in typedic:
        if typedic[key] > precount:
            precount = typedic[key]
            prelabel = key

    print 'true:', truelabel
    print 'predict:', prelabel
    print '-------------'

    if truelabel == prelabel:
        return 1
    else:
        return 0


if __name__ == '__main__':
    # training set: first 100 note
    splitdata(trainsetsize)
    # load label for trainging
    loadlabel()
    # build inverted index with dictionary and list
    buildinvertedindex()
    printinvdict()
    saveinvdict()

    testresult()

