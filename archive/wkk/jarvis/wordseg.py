# -*- coding: utf-8 -*-

import os, sys, codecs, json
import jieba
import jieba.analyse
from snownlp import SnowNLP
import nltk
from nltk.probability import *


# Defaults
config = {
    'root': '~/nomadic',
    'port': 9137,
    'default_notebook': '',
    'override_stylesheet': ''
}

testnote = '../Notes/wdxtub.md'

def nltkproc():
    print 'loading data'
    h = codecs.open(testnote, 'r', 'utf-8')
    text = h.read()
    print 'word segmentation'
    seg_list = jieba.cut(text, cut_all=False)
    print 'turn to nltktext'
    nltktext = nltk.Text(seg_list)
    print 'length:' + str(len(nltktext))
    print 'set:' + str(len(set(nltktext)))
    #fdist = FreqDist(nltktext)
    #fdist.plot(20)
    #nltktext.dispersion_plot([u'笔记',u'支持',u'主题'])
    #nltktext.collocations()
    nltktext.similar(u'笔记')


def keywordtest():
    text = '一页页的阅读，一次次的记录，一本本的书籍，一个个的本子，一条条的新闻，一天天的忘记。这个春节，我花了大量的时间来调研构思设计一个真正能“用”起来的知识管理系统。终于，在假期的最后一天，可以把小小的成果跟大家分享。受《把你的英语用起来》的启发，我想这次，是时候把你的笔记用起来了。'
    tags = jieba.analyse.extract_tags(text, topK=5, withWeight=True)
    for t in tags:
        print t[0] + ' ' + str(t[1])

def wordseg(method):
    cfg_path = os.path.expanduser(u'~/.nomadic')
    # Open the config file.
    with open(cfg_path, 'r') as cfg_file:
        user_cfg = json.load(cfg_file)
        config.update(user_cfg)

    notepath = config['root']

    #testnote = str(notepath + '/wdxtub.md')

    h = codecs.open(testnote, 'r', 'utf-8')
    text = h.read()


    if method == 1:
        seg_list = jieba.cut(text, cut_all=False)
        fh = codecs.open('./seg/test.txt', 'w', 'utf-8')
        fh.write(' '.join(seg_list))
        tags = jieba.analyse.extract_tags(text, topK=10)
        print(",".join(tags))
    elif method == 2:
        s = SnowNLP(text)

        for w in s.keywords(10):
            print w.encode('utf-8')

        for su in s.summary(3):
            print su.encode('utf-8')

    print 'done'




if __name__ == '__main__':
    #wordseg(1)
    #print 'tags'
    #keywordtest()
    print 'nltkproc'
    nltkproc()
