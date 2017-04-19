# -*- coding: utf-8 -*-
from entity import *
import cPickle as pickle

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 统计传入 records 的热门 FAQ
def hotfaqs(records, topK):
    faq_dict = {}
    for r in records:
        if (faq_dict.has_key(r.doctext)):
            faq_dict[r.doctext] = faq_dict[r.doctext] + 1
        else:
            faq_dict[r.doctext] = 1
    result = sorted(faq_dict.items(), key=lambda d: -d[1])[:topK]
    for re in result:
        print re[0].encode('utf-8'),re[1]
    

# 统计传入 records 的热词
def hotwords(records, topK):
    word_dict = {}
    for r in records:
        for w in r.keywords:
            if (word_dict.has_key(w)):
                word_dict[w] = word_dict[w] + 1
            else:
                word_dict[w] = 1
    result = sorted(word_dict.items(), key=lambda d: -d[1])[:topK]
    for re in result:
        print re[0].encode('utf-8'),re[1]

# 统计传入 records 的情感，输出 中性 / 消极
def sentiment(records):
    mid = 0
    neg = 0
    # 给 records 排一下顺序
    result = sorted(records, key=lambda r: r.sentiment)[:10]
    for r in records:
        if (r.sentiment < 0.5):
            neg = neg + 1
        else:
            mid = mid + 1
    print "中性",mid,"/",neg,"消极"
    print "消极率 %.2f %%" %(float(neg)/(float(neg)+float(mid))*100)
    # 最消极的语句
    print "[消极 Top10]"
    for r in result:
        print r.query, r.sentiment

def locationdis(records, topK):
    province_dict = {}
    for r in records:
        if (len(r.province) > 0):
            if (province_dict.has_key(r.province)):
                province_dict[r.province] = province_dict[r.province] + 1
            else:
                province_dict[r.province] = 1
    result = sorted(province_dict.items(), key=lambda d: -d[1])[:topK]
    for re in result:
        print re[0],re[1] 

def showline():
    print "-------------------------------------------"


if __name__=='__main__':
    print "[载入预处理的单日用户 query 数据]"
    f = open("data/rp_records.data")
    records = pickle.load(f)
    f.close()
    
    showline()

    valid_query_count = len(records)
    print "用户有效提问量", valid_query_count

    # 过滤类别，有：
    # 1. 售前
    # 2. 售中
    # 3. 售后
    # 专题类别，有
    # 1. 退货
    # 2. 物流

    prs_count = 0 # 售前
    prs_records = []
    sell_count = 0 # 售中
    sell_records = []
    afs_count = 0 # 售后
    afs_records = []

    return_count = 0 # 退货
    return_records = []
    express_count = 0 # 快递
    express_records = []

    for r in records:
        if (r.doctype.find('售前') != -1):
            prs_count = prs_count + 1
            prs_records.append(r)
        if (r.doctype.find('售中') != -1):
            sell_count = sell_count + 1
            sell_records.append(r)
        if (r.doctype.find('售后') != -1):
            afs_count = afs_count + 1
            afs_records.append(r)
        if (r.doctype.find('退货') != -1):
            return_count = return_count + 1
            return_records.append(r)
        if (r.doctype.find('物流') != -1):
            express_count = express_count + 1
            express_records.append(r)
    
    print "售前的记录 %d (%.2f%%)" % (prs_count, float(prs_count*100) / float(valid_query_count))
    print "售中的记录 %d (%.2f%%)" % (sell_count, float(sell_count*100) / float(valid_query_count))
    print "售后的记录 %d (%.2f%%)" % (afs_count, float(afs_count*100) / float(valid_query_count))
    print "退货的记录 %d (%.2f%%)" % (return_count, float(return_count*100) / float(valid_query_count))
    print "物流的记录 %d (%.2f%%)" % (express_count, float(express_count*100) / float(valid_query_count))


    loc_count = 10
    hot_word_count = 20
    hot_faq_count = 10

    print "------------------ 总体 --------------------"
    print "[省份分布]"
    locationdis(records, loc_count)
    print "[情感]"
    sentiment(records)
    print "[热门FAQ]"
    hotfaqs(records, hot_faq_count)
    print "[热词]"
    hotwords(records, hot_word_count)

    print "------------------ 售前 --------------------"
    print "[省份分布]"
    locationdis(prs_records, loc_count)
    print "[情感]"
    sentiment(prs_records)
    print "[热门FAQ]"
    hotfaqs(prs_records, hot_faq_count)
    print "[热词]"
    hotwords(prs_records, hot_word_count)

    print "------------------ 售中 --------------------"
    print "[省份分布]"
    locationdis(sell_records, loc_count)
    print "[情感]"
    sentiment(sell_records)
    print "[热门FAQ]"
    hotfaqs(sell_records, hot_faq_count)
    print "[热词]"
    hotwords(sell_records, hot_word_count)

    print "------------------ 售后 --------------------"
    print "[省份分布]"
    locationdis(afs_records, loc_count)
    print "[情感]"
    sentiment(afs_records)
    print "[热门FAQ]"
    hotfaqs(afs_records, hot_faq_count)
    print "[热词]"
    hotwords(afs_records, hot_word_count)

    print "------------------ 退货 --------------------"
    print "[省份分布]"
    locationdis(return_records, loc_count)
    print "[情感]"
    sentiment(return_records)
    print "[热门FAQ]"
    hotfaqs(return_records, hot_faq_count)
    print "[热词]"
    hotwords(return_records, hot_word_count)

    print "------------------ 物流 --------------------"
    print "[省份分布]"
    locationdis(express_records, loc_count)
    print "[总体情感]"
    sentiment(express_records)
    print "[热门FAQ]"
    hotfaqs(express_records, hot_faq_count)
    print "[热词]"
    hotwords(express_records, hot_word_count)
    

    
