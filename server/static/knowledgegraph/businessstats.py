# -*- coding: utf-8 -*-
from entity import *
import cPickle as pickle

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

return_dict = {}


def reasons(reason_dict, records, topK):
    result = sorted(reason_dict.items(), key=lambda d: -d[1])
    for re in result:
        print "##########################"
        print re[0].encode('utf-8'), re[1]
        print "##########################"
        print "[省份分布]"
        locationdis(records[re[0]], topK)
        print "[情感]"
        sentiment(records[re[0]])
        print "[热门FAQ]"
        hotfaqs(records[re[0]], topK)
        print "[热词]"
        hotwords(records[re[0]], topK)



# 统计传入 records 的热门 FAQ
def hotfaqs(records, topK):
    faq_dict = {}
    for r in records:
        if (faq_dict.has_key(r.doctext)):
            faq_dict[r.doctext] = faq_dict[r.doctext] + 1
        else:
            faq_dict[r.doctext] = 1
    result = sorted(faq_dict.items(), key=lambda d: -d[1])[:topK]
    
    list1 = []
    for re in result:
        print re[0].encode('utf-8'),re[1]
        list1.append('{"name":"' + re[0].encode('utf-8') + '","value":' + str(re[1]) + '}')
    print ",".join(list1)

    
    

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

    list1 = []
    for re in result:
        print re[0].encode('utf-8'),re[1]
        list1.append('{"name":"' + re[0].encode('utf-8') + '","value":' + str(re[1]) + '}')
    print ",".join(list1)

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
    list1 = []

    for re in result:
        print re.query, re.sentiment
        list1.append("\"" + re.query + "\"")
    print ",".join(list1)


        

def locationdis(records, topK):
    province_dict = {}
    for r in records:
        if (len(r.province) > 0):
            if (province_dict.has_key(r.province)):
                province_dict[r.province] = province_dict[r.province] + 1
            else:
                province_dict[r.province] = 1
    result = sorted(province_dict.items(), key=lambda d: -d[1])[:topK]
    list1 = []
    list2 = []
    for re in result:
        print re[0].encode('utf-8'),re[1]
        list1.append("\"" + re[0] + "\"")
        list2.append(re[1])
    print ",".join(list1)
    print list2


def showline():
    print "-------------------------------------------"

def load_return_dict():
    print "[载入退换货原因分析词典]"
    f = open("data/return_dict.txt")
    for line in f:
        arr = line.split(',')
        for item in arr[1:]:
            # 建立倒排索引
            return_dict[item] = arr[0]
    f.close()
    print "倒排词典数量", len(return_dict)


if __name__=='__main__':
    load_return_dict()

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

    # 退货原因 dict
    return_reason_dict_count = {}
    return_reason_dict_records = {}

    # 圆通，百世
    kdname = ["圆通", "百世", "申通", "顺丰", "韵达", 
    "中通", "EMS", "邮政", "宅急送", "天天", 
    "德邦", "DHL", "全峰", "UPS", "TNT"]
    
    kdcount = [0]*len(kdname)
    # 这样创建才可以，不然都是浅
    kdrecords = [[] for i in range(len(kdname))] 

    for r in records:
        for i in range(len(kdname)):
            if (r.query.find(kdname[i]) != -1):
                kdcount[i] = kdcount[i] + 1
                kdrecords[i].append(r)
        
        arr = r.doctype.split('-')
        if (arr[0].find('售前') != -1):
            prs_count = prs_count + 1
            prs_records.append(r)
        if (arr[0].find('售中') != -1):
            sell_count = sell_count + 1
            sell_records.append(r)
        if (arr[0].find('售后') != -1):
            afs_count = afs_count + 1
            afs_records.append(r)
        if (r.doctype.find('退货') != -1):
            return_count = return_count + 1
            return_records.append(r)
        if (r.doctype.find('物流') != -1):
            express_count = express_count + 1
            express_records.append(r)
        # 属于退货原因图谱
        if (r.docid in return_dict.keys()):
            if (return_reason_dict_count.has_key(return_dict[r.docid])):
                return_reason_dict_count[return_dict[r.docid]] = return_reason_dict_count[return_dict[r.docid]] + 1
                return_reason_dict_records[return_dict[r.docid]].append(r)
            else:
                return_reason_dict_records[return_dict[r.docid]] = []
                return_reason_dict_records[return_dict[r.docid]].append(r)
                return_reason_dict_count[return_dict[r.docid]] = 1

    print "售前的记录 %d (%.2f%%)" % (prs_count, float(prs_count*100) / float(valid_query_count))
    print "售中的记录 %d (%.2f%%)" % (sell_count, float(sell_count*100) / float(valid_query_count))
    print "售后的记录 %d (%.2f%%)" % (afs_count, float(afs_count*100) / float(valid_query_count))
    print "退货的记录 %d (%.2f%%)" % (return_count, float(return_count*100) / float(valid_query_count))
    print "物流的记录 %d (%.2f%%)" % (express_count, float(express_count*100) / float(valid_query_count))

    print "------------------ 快递物流 --------------------"

    for i in range(len(kdname)):
        print "%s 快递被提及次数: %d" % (kdname[i],kdcount[i])




    # loc_count = 12
    # hot_word_count = 20
    # hot_faq_count = 10
    return_count = 10

    #print "------------------ 物流分析 --------------------"
    # 物流分析
    for i in range(len(kdname)):
        if (len(kdrecords[i]) < 50):
            continue
        print "################"
        print kdname[i]
        print "################"
        print len(kdrecords[i])
        # 大于 50 才进行处理分析
        print "[省份分布]"
        locationdis(kdrecords[i], 8)
        print "[情感]"
        sentiment(kdrecords[i])
        print "[热门FAQ]"
        hotfaqs(kdrecords[i], 10)
        print "[热词]"
        hotwords(kdrecords[i], 10)



    #print "------------------ 退货原因 --------------------"
    # 售后原因
    # reasons(return_reason_dict_count, return_reason_dict_records, return_count)


    # print "------------------ 总体 --------------------"
    # print "[省份分布]"
    # locationdis(records, loc_count)
    # print "[情感]"
    # sentiment(records)
    # print "[热门FAQ]"
    # hotfaqs(records, hot_faq_count)
    # print "[热词]"
    # hotwords(records, hot_word_count)

    # print "------------------ 售前 --------------------"
    # print "[省份分布]"
    # locationdis(prs_records, loc_count)
    # print "[情感]"
    # sentiment(prs_records)
    # print "[热门FAQ]"
    # hotfaqs(prs_records, hot_faq_count)
    # print "[热词]"
    # hotwords(prs_records, hot_word_count)

    # print "------------------ 售中 --------------------"
    # print "[省份分布]"
    # locationdis(sell_records, loc_count)
    # print "[情感]"
    # sentiment(sell_records)
    # print "[热门FAQ]"
    # hotfaqs(sell_records, hot_faq_count)
    # print "[热词]"
    # hotwords(sell_records, hot_word_count)

    # print "------------------ 售后 --------------------"
    # print "[省份分布]"
    # locationdis(afs_records, loc_count)
    # print "[情感]"
    # sentiment(afs_records)
    # print "[热门FAQ]"
    # hotfaqs(afs_records, hot_faq_count)
    # print "[热词]"
    # hotwords(afs_records, hot_word_count)

    # print "------------------ 退货 --------------------"
    # print "[省份分布]"
    # locationdis(return_records, loc_count)
    # print "[情感]"
    # sentiment(return_records)
    # print "[热门FAQ]"
    # hotfaqs(return_records, hot_faq_count)
    # print "[热词]"
    # hotwords(return_records, hot_word_count)

    # print "------------------ 物流 --------------------"
    # print "[省份分布]"
    # locationdis(express_records, loc_count)
    # print "[总体情感]"
    # sentiment(express_records)
    # print "[热门FAQ]"
    # hotfaqs(express_records, hot_faq_count)
    # print "[热词]"
    # hotwords(express_records, hot_word_count)
    

    
