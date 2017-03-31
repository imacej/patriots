# -*- coding: utf-8 -*-

import os, sys, codecs, json, re
import cProfile
from yaha import Cuttor, RegexCutting, SurnameCutting, SurnameCutting2, SuffixCutting
from yaha.wordmaker import WordDict
from yaha.analyse import extract_keywords, near_duplicate, summarize1, summarize2, summarize3
import jieba
import jieba.analyse

#testnote = '../Notes/wdxtub.md'
testnote = '../Notes/newstest.md'
bookbase = []
matchbooks = []
# this two sentence can solve Chinese Problem
reload(sys)
sys.setdefaultencoding('utf-8')


def infosum():
    print 'loading data'
    h = codecs.open(testnote, 'r', 'utf-8')

    text = h.read()
    text = re.sub(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d','', text)
    text = re.sub(r'\d\d\d\d-\d\d-\d\d','', text)
    text = re.sub(r'![.*](.*)','',text)
    text = re.sub(r'[.*](.*)','',text)

    print 'keywords:'
    tags = jieba.analyse.extract_tags(text, topK=15)
    print ','.join(tags)
    print 'sum1:'
    print summarize1(text)
    print 'sum2:'
    print summarize2(text)
    print 'sum3:'
    print summarize3(text)
    print 'length:' + str(len(text))
    print 'sum:' + str(len(summarize2(text)))



if __name__ == '__main__':
    infosum()
