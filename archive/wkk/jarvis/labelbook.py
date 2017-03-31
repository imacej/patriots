#coding=utf-8
import os, sys, codecs, json, re

tburl = './seg/books.txt'
tagbase = []

types = [u'技术',u'地理',u'总类',u'科学',u'历史',u'社会',u'人物',u'社会科学',u'宗教',u'文化',u'休闲',u'生活',u'自然',u'科技',u'自然科学']

def printtypes():
    index = 1
    for t in types:
        print str(index), ' ', t
        index = index + 1

def loadtagbase():
    tagfile = codecs.open(tburl, 'r')
    for tagline in tagfile:
        tagbase.append(tagline[:-len('\n')].split('*'))

def labelbook():
    loadtagbase()
    fh = codecs.open('./data/labelbook.txt', 'a', 'utf-8')
    fr = codecs.open('./data/labelbook.txt', 'r', 'utf-8')
    linecount = 0
    for line in fr:
        linecount = linecount + 1

    for line in tagbase:
        if linecount > 0:
            linecount = linecount - 1
            continue

        printtypes()
        book = line[0].decode('utf8')
        print '[', book , ']',
        for tag in line:
            if tag.decode('utf8') == book:
                continue
            print tag,
        print ''
        index = int(raw_input("input the type of the book:\n"))
        temp = book + '#' + types[index-1] + '\n'
        print temp,
        fh.write(temp)


if __name__ == '__main__':
    labelbook()
