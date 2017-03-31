# -*- coding: utf-8 -*-

import os, sys, codecs, json, re
import jieba
import jieba.analyse
import stopwordsfilter

noteroot = '../Notes'
# this two sentence can solve Chinese Problem
reload(sys)
sys.setdefaultencoding('utf-8')

def noteproc():
    files = os.listdir(noteroot)
    taglist = []
    for f in files:
        if f[0] == '.': continue
        if os.path.isdir(noteroot+ '/' + f): continue
        # load note
        h = codecs.open(noteroot+ '/' + f, 'r')
        text = h.read()
        # clean timestamp in notes -> need to be a function
        # TODO eliminate ![]() tag
        #text = re.sub(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d','', text)
        #text = re.sub(r'\d\d\d\d-\d\d-\d\d','', text)
        # clean markdown syntax
        text = re.sub(r'!\[.*\]\(.*\)','',text)
        text = re.sub(r'\(http.*\)','',text)
        text = re.sub(r'#+','', text)
        # get top 15 tags with weights
        tags = jieba.analyse.extract_tags(text, topK=30, withWeight=False)
        # store to a list
        output = f
        print f,

        tags = stopwordsfilter.stopwordsfilter(tags)

        for t in tags:
            print ' ' + t,
            output = output + u' ' + t
        print ''
        taglist.append(output + '\n')

    fh = codecs.open('./seg/tags.txt', 'w', 'utf-8')
    for t in taglist:
        fh.write(t)

    print 'done'

if __name__ == '__main__':
    noteproc()
