# -*- coding: utf-8 -*-

import os, sys, codecs, json, re
import jieba
import jieba.analyse
import stopwordsfilter


testnote = '../Notes/318_tour.md'
bburl = './seg/books.txt'
bookbase = []
matchbooks = []
# this two sentence can solve Chinese Problem
reload(sys)
sys.setdefaultencoding('utf-8')

loglines = []


def loadbookbase():
    bookfile = codecs.open(bburl, 'r')
    for bookline in bookfile:
        bookbase.append(bookline[:-len('\n')].split(' '))

def findsimilarity(note):
    matchbooks = []
    h = codecs.open(note, 'r')
    text = h.read()
    tags = jieba.analyse.extract_tags(text, topK=30)
    loadbookbase()

    tags = stopwordsfilter.stopwordsfilter(tags)

    # start matching
    for bookline in bookbase:
        #tagline is a set of tags for notes
        ismatch = 0
        matchtags = ''
        for tag in tags:
            # tag is one of the tags for testnote
            for mtag in bookline:
                # mtag is one of the tags in one file of the tagbase
                if tag == mtag:
                    # if there is a tag same as the testnote's tag, we add it to the list
                    ismatch = 1
                    matchtags = matchtags + tag + " "
                    break
        if ismatch == 1:
            matchbooks.append(bookline[0] + " " + matchtags)

    print 'Original Notes'
    print note
    loglines.append('Original Notes: ' + note + '\n')
    print 'Related Books:'
    loglines.append('Related Books:' + '\n')
    for book in matchbooks:
        loglines.append(book + '\n')
        print book
    loglines.append('-------------------')

if __name__ == '__main__':


    noteroot = '../Notes/'
    notes = os.listdir(noteroot)
    count = 0

    for note in notes:
        if note[0] == '.':
            continue
        print 'processing ' + note
        findsimilarity(noteroot + note)

    fh = codecs.open('./result/simbooks.txt', 'w', 'utf-8')
    for line in loglines:
        fh.write(line)

    print 'done'
