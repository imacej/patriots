# -*- coding: utf-8 -*-
from entity import *
import cPickle as pickle
 

# 先做奶粉

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
        print re[0],re[1] 

# 统计传入 records 的情感，输出 中性 / 消极
def sentiment(records):
    mid = 0
    neg = 0
    for r in records:
        if (r.sentiment < 0.5):
            neg = neg + 1
        else:
            mid = mid + 1
    print "中性",mid,"/",neg,"消极"
    print "消极率 %.2f %%" %(float(neg)/(float(neg)+float(mid))*100)


def locationdis(records):
    province_dict = {}
    for r in records:
        if (len(r.province) > 0):
            if (province_dict.has_key(r.province)):
                province_dict[r.province] = province_dict[r.province] + 1
            else:
                province_dict[r.province] = 1
    result = sorted(province_dict.items(), key=lambda d: -d[1])
    for re in result:
        print re[0],re[1] 


def showline():
    print "-------------------------------------------"

if __name__=='__main__':
    print "[载入预处理的单日用户 query 数据]"
    f = open("data/records.data")
    records = pickle.load(f)
    f.close()
    print "有效的记录数量", len(records)
    
    showline()

    print "[载入奶粉品牌词典]"
    mp_brands = []
    f = open("data/mpbrand.txt")
    for line in f:
        arr = line.split(' ')
        mp_brands.append(arr[0])
    f.close()
    print "品牌数量", len(mp_brands)

    showline()

    # 过滤类别，有：
    # 1. 总类
    # 2. 总类内售前
    # 3. 总类内售中
    # 4. 总类内售后
    # 5. 总类内全球购
    # 6. 总类内品牌
    k_count = 0 # 匹配到知识节点
    mp_count = 0 # 匹配到奶粉的节点
    mp_records = []
    
    print "[过滤奶粉总类]"
    
    length = len(records)
    for i, r in enumerate(records):
        if (len(r.knodes) > 0):
            k_count = k_count + 1
            if ('奶粉' in r.knodes):
                mp_count = mp_count + 1
                mp_records.append(r)
                #r.displayRecord()

    print "匹配到知识图谱节点的记录",k_count,"/",length
    print "匹配到奶粉节点的记录",mp_count,"/",length

    showline()

    mp_pos_count = 0

    print "[省份分布]"
    for r in mp_records:
        if (len(r.province) > 0):
            mp_pos_count = mp_pos_count + 1
            # r.displayRecord()
    print "含有位置的奶粉记录", mp_pos_count ,"/", mp_count
    locationdis(mp_records)

    showline()

    mp_prs_count = 0 # 售前
    mp_prs_records = []
    mp_sell_count = 0 # 售中
    mp_sell_records = []
    mp_afs_count = 0 # 售后
    mp_afs_records = []
    mp_gbs_count = 0 # 全球购
    mp_gbs_records = []
    print "[售前中后、全球购统计]"
    print "部分 FAQ 分类中同时包含 售前 售中 售后 全球购 的两个或以上，所以与总数不一致"
    for r in mp_records:
        if (r.doctype.find('售前') != -1):
            mp_prs_count = mp_prs_count + 1
            mp_prs_records.append(r)
        if (r.doctype.find('售中') != -1):
            mp_sell_count = mp_sell_count + 1
            mp_sell_records.append(r)
        if (r.doctype.find('售后') != -1):
            mp_afs_count = mp_afs_count + 1
            mp_afs_records.append(r)
        if (r.doctype.find('全球购') != -1):
            mp_gbs_count = mp_gbs_count + 1
            mp_gbs_records.append(r)

    print "奶粉售前的记录",mp_prs_count,"/",mp_count
    print "奶粉售中的记录",mp_sell_count,"/",mp_count
    print "奶粉售后的记录",mp_afs_count,"/",mp_count
    print "奶粉全球购的记录",mp_gbs_count,"/",mp_count

    showline()

    mp_brand_dict = {}
    mp_brand_count = 0
    print "[品牌统计]"
    for r in mp_records:
        for b in mp_brands:
            if (r.query.find(b) != -1): 
                mp_brand_count = mp_brand_count + 1
                # 如果找到对应品牌，则加入到品牌列表
                if (mp_brand_dict.has_key(b)):
                    mp_brand_dict[b].append(r)
                else:
                    tmp = []
                    tmp.append(r)
                    mp_brand_dict[b] = tmp
    print "包含奶粉品牌的记录", mp_brand_count,"/",mp_count
    for key in mp_brand_dict.keys():
        print key, len(mp_brand_dict[key]),"/",mp_brand_count

    showline()
    print "[奶粉总体情感]"
    sentiment(mp_records)
    print "[奶粉总体热词]"
    hotwords(mp_records, 15)
    
    showline()
    print "[奶粉售前总体情感]"
    sentiment(mp_prs_records)
    print "[奶粉售前总体热词]"
    hotwords(mp_prs_records, 15)

    showline()
    print "[奶粉售中总体情感]"
    sentiment(mp_sell_records)
    print "[奶粉售中总体热词]"
    hotwords(mp_sell_records, 15)

    showline()
    print "[奶粉售后总体情感]"
    sentiment(mp_afs_records)
    print "[奶粉售后总体热词]"
    hotwords(mp_afs_records, 15)

    showline()
    print "[奶粉全球购情感]"
    sentiment(mp_gbs_records)
    print "[奶粉全球购总体热词]"
    hotwords(mp_gbs_records, 15)



