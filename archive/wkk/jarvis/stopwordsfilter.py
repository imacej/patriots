# -*- coding: utf-8 -*-
import os, sys, codecs, json, re
import jieba
import jieba.analyse

stopwordslist = [u'之后',u'然后',u'可以',u'他们',u'不要',u'一旦',u'如果',u'一个',u'所以',u'比如',u'我们',u'因为',u'但是',u'并且',u'大概',u'总是',u'就是',u'一向',u'能够',u'便是',u'没有',u'可是',u'往往',u'不是',u'一种',u'或者',u'什么',u'别人',u'很多',u'不能',u'某个',u'那些',u'当时',u'于是',u'可能',u'非常',u'自己',u'还是',u'何必',u'以及',u'很多',u'带来',u'几个',u'几乎',u'不仅',u'总会',u'时候',u'这种',u'应该',u'任何',u'那些',u'这些',u'下列',u'那么',u'为什么',u'无法',u'这个',u'什么样',u'每个',u'它们',u'不可',u'一定',u'只有',u'只要',u'他人',u'人们',u'这个',u'或是',u'这样',u'是因为',u'一本',u'对于',u'一些',u'每个',u'水儿',u'这手',u'已经',u'因此',u'甚至',u'我会',u'一点',u'做些',u'不如',u'我果',u'之心',u'不禁',u'四句',u'一遍',u'只是',u'同时',u'必须',u'觉得',u'知道',u'脸来',u'六个',u'不会',u'变为',u'之间',u'人会',u'一起',u'第十',u'凡是',u'定然',u'定有',u'来说',u'更加',u'其实',u'从来',u'这么样',u'一股',u'好像',u'她们',u'第五',u'第四',u'一次',u'一场',u'无论',u'人若',u'接著',u'全在',u'点至',u'哪里',u'就要',u'一件',u'咱们',u'片中',u'这项',u'最初',u'在于',u'这张',u'当然',u'不了',u'他会',u'同样',u'这串',u'并非',u'而是',u'也许',u'人来',u'多么',u'那位',u'此者',u'一组',u'这一',u'反而',u'而是',u'如此',u'所在',u'就算',u'有要',u'100',u'25',u'80',u'10',u'15',u'11',u'20',u'000']

def stopwordsfilter(tags):
    rtntags = []
    find = 0
    for tag in tags:
        find = 0
        for sw in stopwordslist:
            if tag == sw:
                find = 1
                break
        if find == 0:
            rtntags.append(tag)

    return rtntags

if __name__ == '__main__':
    note = '../Notes/318_tour.md'
    h = codecs.open(note, 'r')
    text = h.read()
    tags = jieba.analyse.extract_tags(text, topK=15)
    for tag in stopwordsfilter(tags):
        print tag + ' '
