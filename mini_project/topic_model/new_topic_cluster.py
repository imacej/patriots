# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import numpy as np
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
from scipy import *
from sys import argv
import jieba
import codecs
import datetime
import time
import re
import xlrd
import csv
from optparse import OptionParser
import os, sys
reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

documents = []
hidden_vectors = []

# 不同业务需要配置不同的词典，效果比较好
# 在停止词中添加的内容，同样需要添加到对应的词典中，这样才能分词出来
# 更新词表后，需要重新分词

word_freq_file = "stat/word_freq.txt"  # 词频统计

split_query = "query/query_fangtai_split"  # 方太分词后的文件

knowledge_data = "knowledge_data/baiyushuang.xls"
knowledge_result = "knowledge_data/baiyushuang_result.txt"

query_gap = 10 # 一个类中多少条内容的界限
topic_distance_max = 999999 # 类方差

topic_dict_path = "query/topic%d.dict"
topic_query = "query/topic_query"  # 每个 topic 的 query，用于二次 LDA 聚类
topic_result = "topic_result"
lda_model = "model/lda_model"
lda_model_topic = "model/lda_model_topic"
lsi_model = "model/lsi_model"

lda_result_dir = "lda_result/"
lsi_result_dir = "lsi_result/"
kmeans_result_dir = "kmeans_result/"
ap_result_dir = "ap_result/"

dirs = [lda_result_dir, lsi_result_dir, kmeans_result_dir, ap_result_dir]

# 如果不存在则创建
for i, val in enumerate(dirs):
    if os.path.exists(val) == False:
        os.mkdir(val) 

num_sub_topic = 0
num_topn = 40  # get topic terms 的词个数
final_a = 200  # topic 评分中 doc 的系数
final_b = 100  # topic 评分中 word 的系数
min_word_count = 15  # 分期的数据人名较多，过滤掉
max_sentence_length = 400  # 这个值如果数值大

# 保证每次结果一致
FIXED_SEED = 44
np.random.seed(FIXED_SEED)

def CheckRet(ret):
    if 0 == ret:
		return
    print "返回值错误: %d" % ret
    exit(1)

# KL 散度
# 需要传入俩 numpy array

def asymmetricKL(P, Q):
    return sum(P * log(P / Q))  # calculate the kl divergence between P and Q

# KL 散度
def symmetricalKL(P, Q):
    return (asymmetricKL(P, Q) + asymmetricKL(Q, P)) / 2.00


def tokenize_query(raw_query, show_count, user_dict, tokenized_query):
    print "开始读取原始用户问句日志，之后分词并保存到文件中"
    
    if raw_query is None:
        print "没有指定原始数据，请使用 --raw_query 选项指定"
        return 1

    count = 0
    jieba.load_userdict(user_dict)
    with open(raw_query) as fr:
        for line in fr:
            if (len(line) < min_word_count):
                # 处理空行和长度小于 6 的
                continue
            if (len(line) > max_sentence_length):
                # 太长的去掉
                continue
            # 去掉空格
            arr = line.split(" ")
            seg_list = jieba.cut("".join(arr))  # 默认是精确模式
            documents.append(" ".join(seg_list))
            count = count + 1
            if (count % show_count == 0):
                print "已处理 %d 行" % count
    print "日志共 %d 条有效记录" % count
    with codecs.open(tokenized_query, "w+", "utf-8") as f:
        for doc in documents:
            f.write(doc)
    print "写入到文件 %s 完成" % tokenized_query
    return 0


def load_raw_query(raw_query):
    print "载入原始数据到内存中（不分词不过滤）"

    if raw_query is None:
        print "没有指定原始数据，请使用 --raw_query 选项指定"
        return 1

    count = 0
    with open(raw_query) as fr:
        for line in fr:
            # 处理下每一行，如果是分词后的，合起来，如果有换行，去掉
            arr = line.split(' ')
            newline = "".join(arr)
            newline = newline.replace("\n", "")
            newline = newline.replace("\r", "")
            documents.append(newline)
            count = count + 1
    print "共 %d 条日志记录" % count
    return 0


def load_hidden_vector(raw_query, hidden_vector):
    print "载入对应 %s 的隐藏向量" % raw_query
    if hidden_vector is None:
        print "没有指定隐藏向量，请使用 --hidden_vector 选项指定"
        return 1

    count = 0
    with open(hidden_vector) as fr:
        for line in fr:
            hidden_vectors.append(line)
            count = count + 1
    print "共 %d 个隐藏向量" % count
    return 0


def load_tokenized_query(tokenized_query):
    print "载入处理后的分词数据"
    with open(tokenized_query) as fr:
        for line in fr:
            documents.append(line)
    print "日志共 %d 条有效记录" % len(documents)
    return 0


def load_topic_query(topicid):
    print "载入 topic %d 的分词数据" % topicid
    count = 0
    topic_docs = []
    with open("%s%d" % (topic_query, topicid)) as f:
        for line in f:
            topic_docs.append(line)
            count = count + 1
    print "topic %d 共有 %d 条有效记录" % (topicid, len(topic_docs))
    return topic_docs


def get_stoplist(stop_words):
    stoplist = set()
    # 载入停止词
    with codecs.open(stop_words, "r+", "utf-8") as f:
        for word in f:
            stoplist.add(word[:-1])  # 去掉最后的回车符号
    print "停止词共 %d 个" % len(stoplist)
    return stoplist


def get_texts(stop_words):
    stoplist = get_stoplist(stop_words)
    # remove words and tokenize
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # for i in range(10):
    #     print " ".join(texts[i])

    # remove words that appear only once
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    # 去掉长度大于 6 的词
    texts = [[token for token in text if len(token) <= 6]
             for text in texts]

    # 删掉空行
    tmp = []
    for text in texts:
        # 至少需要俩词
        if (len(text) > 1):
            tmp.append(text)

    texts = tmp

    print "全量语料已载入，共 %d 条" % len(texts)
    return texts


def get_topic_texts(topicid):
    stoplist = get_stoplist()
    topic_docs = load_topic_query(topicid)
    texts = [[unicode(word, "utf-8") for word in doc.lower().split() if unicode(word, "utf-8") not in stoplist]
             for doc in topic_docs]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # remove words that appear only once
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    # 去掉长度大于 6 的词
    texts = [[token for token in text if len(token) <= 6]
             for text in texts]

    # 删掉空行
    tmp = []
    for text in texts:
        # 至少需要俩词
        if (len(text) > 1):
            tmp.append(text)
    texts = tmp

    print "topic %d 的语料已载入，共 %d 条" % (topicid, len(texts))
    return texts


def generate_dict(query_dict, stop_words):
    texts = get_texts(stop_words)
    # store the dictionary for future referece
    dictionary = corpora.Dictionary(texts)
    dictionary.save(query_dict)
    print "词典已保存到 %s 文件中" % query_dict
    return 0


def generate_topic_dict(topicid):
    texts = get_topic_texts(topicid)
    dictionary = corpora.Dictionary(texts)
    path = topic_dict_path % topicid
    dictionary.save(path)
    print "topic %d 词典已保存到 %s 文件中" % (topicid, path)


def generate_lsi_topic(query_dict, stop_words, num_topic):
     # 载入词典
    dictionary = corpora.Dictionary.load(query_dict)
    print "载入词典完成"

    # 载入语料
    texts = get_texts(stop_words)

    begin = datetime.datetime.now()
    corpus = [dictionary.doc2bow(text) for text in texts]

    print "开始训练 LSI 模型，共 %d 个 topic" % num_topic
    LSI = models.LsiModel(corpus, num_topics=num_topic,
                          id2word=dictionary, chunksize=2000)

    end = datetime.datetime.now()
    print "处理 LSI 用时", end - begin

    # 保存 LDA 模型
    LSI.save(lsi_model)
    print "模型已保存到 %s 中" % lsi_model
    return 0


def generate_lda_sub_topic(topicid):
    # 载入词典
    dictionary = corpora.Dictionary.load(topic_dict_path % topicid)
    print "载入 topic %d 词典完成" % topicid

    # 载入语料
    texts = get_topic_texts(topicid)

    begin = datetime.datetime.now()
    corpus = [dictionary.doc2bow(text) for text in texts]
    # store to disk, for later use
    # corpora.MmCorpus.serialize('./nanfang.mm', corpus)
    # 单核
    # LDA = models.LdaModel(corpus, id2word=dictionary, num_topics=200, update_every=1, minimum_probability=0.1, passes=5)
    # 多核
    # models.ldamulticore.LdaMulticore(corpus, num_topics=200, id2word=dictionary, workers=None, chunksize=2000, passes=1, batch=False, alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10, iterations=50, gamma_threshold=0.001)
    print "开始训练 topic %d 的子 topic，共 %d 个" % (topicid,  num_sub_topic)
    LDA = models.LdaMulticore(corpus, num_topics=num_sub_topic,
                              id2word=dictionary, workers=4, chunksize=2000, passes=1)
    end = datetime.datetime.now()
    print "训练用时", end - begin

    # 保存 LDA 模型
    path = "%s%d" % (lda_model_topic, topicid)
    LDA.save(path)
    print "topic %d 模型已保存到 %s 中\n" % (topicid, path)


def generate_lda_topic(query_dict, stop_words, num_topic):
    # 载入词典
    dictionary = corpora.Dictionary.load(query_dict)
    print "载入词典完成"

    # 载入语料
    texts = get_texts(stop_words)

    begin = datetime.datetime.now()
    corpus = [dictionary.doc2bow(text) for text in texts]
    # store to disk, for later use
    # corpora.MmCorpus.serialize('./nanfang.mm', corpus)
    # 单核
    # LDA = models.LdaModel(corpus, id2word=dictionary, num_topics=200, update_every=1, minimum_probability=0.1, passes=5)
    # 多核
    # models.ldamulticore.LdaMulticore(corpus, num_topics=200, id2word=dictionary, workers=None, chunksize=2000, passes=1, batch=False, alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10, iterations=50, gamma_threshold=0.001)
    
    # 单层
    print "开始训练 LDA 模型，共 %d 个 topic" % num_topic
    # 多层
    # print "开始训练第一层 LDA 模型，共 %d 个 topic" % num_topic
    LDA = models.LdaMulticore(corpus, num_topics=num_topic,
                              id2word=dictionary, workers=4, chunksize=2000, passes=5)
    
    # 多层
    # level1 = datetime.datetime.now()
    # print "第一层 LDA 模型训练完成，用时", level1 - begin

    # 分离每个 topic 的数据
    # topic_text = [[] for i in range(num_topic)]
    # print "开始分离各个 topic 的数据"
    # for i in range(len(texts)):
    #     if (i % 10000 == 0):
    #         print "正在处理第 %d 行" % i
    #     # 获取每个文本的 topics
    #     topics = LDA.get_document_topics(corpus[i])
    #     # 这里选择 Top1
    #     if (len(topics) < 1):
    #         continue
    #     # print len(topics), topics[0]
    #     topic_text[topics[0][0]].append(" ".join(texts[i]))

    # 写入每个 topic 的数据
    # for i in range(num_topic):
    #     print "写入 topic %d 的用户问句（已分词）" % i
    #     with codecs.open("%s%d" %(topic_query, i), "w+", "utf-8") as f:
    #         for line in topic_text[i]:
    #             if (len(line) > 1):
    #                 f.write(line+"\n")

    # 写入子 topic
    # for i in range(num_topic):
    #     generate_topic_dict(i) # 生成词典
    #     generate_sub_topic(i) # 生成 子 topic

    end = datetime.datetime.now()
    print "处理 LDA 用时", end - begin

    # 保存 LDA 模型
    LDA.save(lda_model)
    print "模型已保存到 %s 中" % lda_model
    return 0


def clean_topic(line):
    # 用来清理 topic 的显示
    # example 0.075*"投" + 0.060*"失败" + 0.059*"智定" + 0.043*"邮政" + 0.036*"持仓" + 0.030*"开通" + 0.029*"定" + 0.025*"为什么" + 0.023*"支付" + 0.022*"卡"
    newline = []
    arr = line.split('+')
    for item in arr:
        words = item.split("\"")
        newline.append(words[1])
    return " ".join(newline)


def show_lda_topic_document(rankid, topicid):
    dictionary = corpora.Dictionary.load(topic_dict_path % topicid)
    print "载入 topic %d 词典完成" % topicid

    # 载入语料
    texts = get_topic_texts(topicid)

    corpus = [dictionary.doc2bow(text) for text in texts]
    print "Corpus 数量 %d" % len(corpus)

    # 载入模型
    LDA = models.LdaModel.load("%s%d" % (lda_model_topic, topicid))

    # 创建不同的数组，根据 topic 来排序
    topic_result = [{} for i in range(num_sub_topic)]
    for i in range(len(texts)):
        if (i % 1000 == 0):
            print "正在处理第 %d 行" % i
        # 获取每个文本的 topics
        topics = LDA.get_document_topics(corpus[i])
        # 这里选择 Top1
        if (len(topics) < 1):
            continue
        # print len(topics), topics[0]
        topic_result[topics[0][0]]["".join(texts[i])] = topics[0][1]

    # 对每个 topic 进行打分
    topic_rank = []
    for i in range(num_sub_topic):
        if (len(topic_result[i]) < 1):
            continue

        temp_doc_vector = []
        # doc score 背景噪声向量
        doc_bg_vector = np.array(
            [1.0 / len(topic_result[i])] * len(topic_result[i]))
        # 得出 doc score 向量
        for record in topic_result[i].items():
            temp_doc_vector.append(record[1])  # 加入各个概率
        # 得出最终概率向量
        doc_vector = np.array(temp_doc_vector) / sum(temp_doc_vector)

        temp_word_vector = []
        # word score 背景噪声向量
        word_bg_vector = np.array([1.0 / num_topn] * num_topn)
        # 得出 word score 向量
        for item in LDA.get_topic_terms(i, topn=num_topn):
            temp_word_vector.append(item[1])
        word_vector = np.array(temp_word_vector)

        # 计算分数并放到数组中
        doc_score = asymmetricKL(doc_vector, doc_bg_vector)
        word_score = asymmetricKL(word_vector, word_bg_vector)
        final_score = final_a * doc_score + final_b + word_score
        # print i, final_score, doc_score, word_score
        topic_rank.append((i, final_score))

    # 根据分值进行排序输出
    # 对每个字典进行排序
    ranks = sorted(topic_rank, key=lambda d: -d[1])

    for i in range(len(ranks)):
        line = LDA.print_topic(ranks[i][0], topn=num_topn)
        line1 = "[Rank %d Topic %d SubRank %d SubTopic %d] %s" % (
            rankid, topicid, i, ranks[i][0], clean_topic(line))
        line2 = "分值 %f 共 %d 条 query" % (
            ranks[i][1], len(topic_result[ranks[i][0]]))
        print line1
        print line2

        # 根据概率排序
        result = sorted(topic_result[ranks[i][0]].items(), key=lambda d: -d[1])

        # 写入到对应文本中
        # 这里应该按照顺序写入
        filepath = "%srank%d-%d.txt" % (lda_result_dir, rankid, i)
        with codecs.open(filepath, "w+", "utf-8") as f:
            f.write("%s\n%s\n" % (line1, line2))
            f.write("----------------------\n")
            for re in result:
                f.write("%f %s\n" % (re[1], re[0]))
        print "写入 %s 完成" % filepath
        print "----------------------"


def show_lda_document(query_dict, stop_words, num_topic, show_count):
    # 载入词典
    dictionary = corpora.Dictionary.load(query_dict)
    print "载入词典完成"

    # 载入语料
    texts = get_texts(stop_words)

    corpus = [dictionary.doc2bow(text) for text in texts]
    print "Corpus 数量 %d" % len(corpus)

    LDA = models.LdaModel.load(lda_model)
    print "载入 LDA 模型完成"

    # 创建不同的数组，根据 topic 来排序
    topic_result = [{} for i in range(num_topic)]
    for i in range(len(texts)):
        if (i % show_count == 0):
            print "正在处理第 %d 行" % i
        # 获取每个文本的 topics
        topics = LDA.get_document_topics(corpus[i])
        # 这里选择 Top1
        if (len(topics) < 1):
            continue
        # print len(topics), topics[0]
        topic_result[topics[0][0]]["".join(texts[i])] = topics[0][1]

        # 这里是全量数据
        # for j in range(len(topics)):
        #     # 分配到不同的 topics 中
        #     topic_result[topics[j][0]][texts[i]] = topics[j][1]

    # 对每个 topic 进行打分
    topic_rank = []
    for i in range(num_topic):
        if (len(topic_result[i]) < 1):
            continue
        temp_doc_vector = []
        # doc score 背景噪声向量
        doc_bg_vector = np.array(
            [1.0 / len(topic_result[i])] * len(topic_result[i]))
        # 得出 doc score 向量
        for record in topic_result[i].items():
            temp_doc_vector.append(record[1])  # 加入各个概率
        # 得出最终概率向量
        doc_vector = np.array(temp_doc_vector) / sum(temp_doc_vector)

        temp_word_vector = []
        # word score 背景噪声向量
        word_bg_vector = np.array([1.0 / num_topn] * num_topn)
        # 得出 word score 向量
        for item in LDA.get_topic_terms(i, topn=num_topn):
            temp_word_vector.append(item[1])
        word_vector = np.array(temp_word_vector)

        # 计算分数并放到数组中
        doc_score = asymmetricKL(doc_vector, doc_bg_vector)
        word_score = asymmetricKL(word_vector, word_bg_vector)
        final_score = final_a * doc_score + final_b + word_score
        # print i, final_score, doc_score, word_score
        topic_rank.append((i, final_score))

    # 根据分值进行排序输出
    # 对每个字典进行排序
    ranks = sorted(topic_rank, key=lambda d: -d[1])

    for i in range(len(ranks)):
        line = LDA.print_topic(ranks[i][0], topn=num_topn)
        line1 = "[Rank %d Topic %d] %s" % (i, ranks[i][0], clean_topic(line))
        line2 = "分值 %f 共 %d 条 query" % (
            ranks[i][1], len(topic_result[ranks[i][0]]))
 
        # 根据概率排序
        result = sorted(topic_result[ranks[i][0]].items(), key=lambda d: -d[1])

        # 写入到对应文本中
        # 这里应该按照得分顺序写入，加一个 - 用来排序
        filepath = "%srank%03d.txt" % (lda_result_dir, i)
        with codecs.open(filepath, "w+", "utf-8") as f:
            f.write("%s\n%s\n" % (line1, line2))
            f.write("----------------------\n")
            for re in result:
                f.write("%f %s\n" % (re[1], re[0]))
        print "写入 %s 完成" % filepath
        print "----------------------"

        # 读入这个分类下的子分类
        # show_lda_topic_document(i, ranks[i][0])
    return 0

def show_lsi_document(query_dict, stop_words, num_topic):
     # 载入词典
    dictionary = corpora.Dictionary.load(query_dict)
    print "载入词典完成"

    # 载入语料
    texts = get_texts(stop_words)

    corpus = [dictionary.doc2bow(text) for text in texts]
    print "Corpus 数量 %d" % len(corpus)

    LSI = models.LsiModel.load(lsi_model)
    print "载入 LSI 模型完成"

    filepath = "%slsi-topics.txt" % lsi_result_dir
    with codecs.open(filepath, "w+", "utf-8") as f:
        for i in range(num_topic):
            topic = LSI.show_topic(i, topn=40)
            f.write("---------------------\n")
            f.write("Topic %d\n" % i)
            for term in topic:
                f.write("%s %f\n" % (term[0], term[1]))

    # 得到文档的向量，共 num_topic 维，生成测试数据
    print "生成文档向量"
    # 这里的格式需要处理 类型不同

    X = np.zeros((len(corpus), num_topic))

    for i in range(len(corpus)):
        vline = LSI[corpus[i]]
        for j in range(len(vline)):
            X[i][j] = vline[j][1]

    print "归一化数据集（特征选择）"
    # normalized dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    kmeans = cluster.MiniBatchKMeans(n_clusters=num_topic)
    #affinity_propagation = cluster.AffinityPropagation(damping=.5, preference=None)

    t0 = datetime.datetime.now()
    print "开始 Kmean 聚类，中心个数 %d" % num_topic
    kmeans.fit(X)
    # print "开始 AP 聚类，中心个数 %d" % num_topic
    # affinity_propagation.fit(X)
    t1 = datetime.datetime.now()
    print "聚类耗时", t1 - t0

    # 输出结果
    print "按照类别写入到结果中"
    y_pred = kmeans.labels_.astype(np.int)
    #y_pred = affinity_propagation.labels_.astype(np.int)

    # 聚类中心
    centers = kmeans.cluster_centers_
    print centers

    # 找到类别中的最大值
    maxY = max(y_pred)
    print "类别个数", maxY + 1

    # 各个类别的结果
    # 也写入到一个统一的文件中
    resultpath = "%sresult_all.txt" % lsi_result_dir
    topic_ranks = []
    with codecs.open(resultpath, "w+", "utf-8") as r:
        topic_result = [{} for i in range(maxY + 1)]
        for i in range(len(texts)):
            dist = np.linalg.norm(centers[y_pred[i]].astype(
                'float64') - X[i].astype('float64'))
            topic_result[y_pred[i]][documents[i]] = dist
        print "写入结果..."
        print "计算类的平均方差"
        for i in range(len(topic_result)):
            # 给每个类算方差
            
            total = 0.0
            count = 0.0
            # 如果一个类中少于 10 条内容，统一设为一个极大值
            if len(topic_result[i]) < query_gap :
                topic_ranks.append((i, topic_distance_max))
                continue
            # 如果大于阈值，则需要计算
            for item in topic_result[i].items():
                total += item[1]*item[1]
                count += 1
            topic_ranks.append((i, total/count))
        # 给结果排序
        print "给结果排序"
        sorted_ranks = sorted(topic_ranks, key=lambda item: item[1])
            
        for i in range(len(sorted_ranks)):
            filepath = "%stopic%03d.txt" % (lsi_result_dir, i)
            print "写入类别 %d 至 %s" % (i, filepath)
            with codecs.open(filepath, "w+", "utf-8") as f:
                r.write("类别 %d 的记录个数 %d\n" % (i, len(topic_result[sorted_ranks[i][0]])))
                f.write("类别 %d 的记录个数 %d\n" % (i, len(topic_result[sorted_ranks[i][0]])))
                r.write("类方差 %f\n" % sorted_ranks[i][1]) 
                f.write("类方差 %f\n" % sorted_ranks[i][1])
                #r.write("聚类中心 %s\n" % np.array2string(centers[i]))
                #f.write("聚类中心 %s\n" % np.array2string(centers[i]))
                sorted_list = sorted(
                    topic_result[sorted_ranks[i][0]].items(), key=lambda item: item[1])
                for line in sorted_list:
                    iline = "".join(line[0].split(" ")).replace("\n","")
                    f.write("%f %s\n" % (line[1], iline))
                    r.write("%f %s\n" % (line[1], iline))
                # 总文件加个分隔符
                r.write("===============================================\n")
        print "LSI 结果处理完成"
    return 0

# python new_topic_cluster.py --raw_query=query/fangtai.txt --hidden_vector=query/fangtai.hidden kmeans
def cluster_query(method, raw_query, hidden_vector, num_topic):
    
    # 用来聚类杨老师那边给出的数据
    CheckRet(load_raw_query(raw_query))
    CheckRet(load_hidden_vector(raw_query, hidden_vector))
    # 检测数量匹配
    if (len(documents) != len(hidden_vectors)):
        print "日志数量与向量数量不符，请检查后重试"
        return 1

    # 接下来是正常处理流程
    print "生成隐藏向量数组"
    t0 = datetime.datetime.now()
    X = np.array([[ele for ele in vector[:-1].split("\t")]
                  for vector in hidden_vectors])
    t1 = datetime.datetime.now()
    print "耗时", t1 - t0

    # print "归一化数据集（特征选择）"
    # # normalized dataset for easier parameter selection
    # t0 = datetime.datetime.now()
    # X = StandardScaler().fit_transform(X)
    # t1 = datetime.datetime.now()
    # print "耗时", t1-t0

    if (method == "kmeans"):
        print "开始 %s 聚类，中心个数 %d" % (method, num_topic)
        algorithm = cluster.MiniBatchKMeans(n_clusters=num_topic)
    elif (method == "ap"):
        print "开始 %s 聚类，中心个数待定" % method
        algorithm = cluster.AffinityPropagation(damping=.5, preference=None)

    t0 = datetime.datetime.now()
    algorithm.fit(X)
    t1 = datetime.datetime.now()
    print "耗时", t1 - t0

    # 输出结果
    print "按照类别写入到结果中"
    y_pred = algorithm.labels_.astype(np.int)

    # 聚类中心
    centers = algorithm.cluster_centers_
    print centers

    # 找到类别中的最大值
    maxY = max(y_pred)
    print "类别个数", maxY + 1

    # 各个类别的结果
    # 也写入到一个统一的文件中
    resultpath = "%sresult_all.txt" % kmeans_result_dir
    topic_ranks = []
    with codecs.open(resultpath, "w+", "utf-8") as r:
        topic_result = [{} for i in range(maxY + 1)]
        print "计算文档到类中心的距离..."
        for i in range(len(documents)):
            dist = np.linalg.norm(centers[y_pred[i]].astype(
                'float64') - X[i].astype('float64'))
            topic_result[y_pred[i]][documents[i]] = dist
        print "写入结果..."
        print "计算类的平均方差"
        for i in range(len(topic_result)):
            # 给每个类算方差
            total = 0.0
            count = 0.0
            # 如果一个类中少于 10 条内容，统一设为一个极大值
            if len(topic_result[i]) < query_gap :
                topic_ranks.append((i, topic_distance_max))
                continue
            # 如果大于阈值，则需要计算
            for item in topic_result[i].items():
                total += item[1]*item[1]
                count += 1
            topic_ranks.append((i, total/count))
        # 给结果排序
        print "给结果排序"
        sorted_ranks = sorted(topic_ranks, key=lambda item: item[1])
        for i in range(len(sorted_ranks)):
            filepath = "%stopic%03d.txt" % (kmeans_result_dir, i)
            print "写入类别 %d 至 %s" % (i, filepath)
            with codecs.open(filepath, "w+", "utf-8") as f:
                r.write("类别 %d 的记录个数 %d\n" % (i, len(topic_result[sorted_ranks[i][0]])))
                f.write("类别 %d 的记录个数 %d\n" % (i, len(topic_result[sorted_ranks[i][0]])))
                r.write("类方差 %f\n" % sorted_ranks[i][1]) 
                f.write("类方差 %f\n" % sorted_ranks[i][1])
                #r.write("聚类中心 %s\n" % np.array2string(centers[i]))
                #f.write("聚类中心 %s\n" % np.array2string(centers[i]))
                # 排序并输出
                sorted_list = sorted(
                    topic_result[sorted_ranks[i][0]].items(), key=lambda item: item[1])
                for line in sorted_list:
                    iline = "".join(line[0].split(" ")).replace("\n","")
                    f.write("%f %s\n" % (line[1], iline))
                    r.write("%f %s\n" % (line[1], iline))
                # 总文件加个分隔符
                r.write("===============================================\n")
    print "聚类结果处理完成"
    return 0

# 这里最好需要进行一步 dos2unix filename 转换换行符


def word_freq():
    total = len(documents)
    print "统计 %d 条数据的词频" % total
    t0 = datetime.datetime.now()
    word_dict = {}
    i = 0
    word_count = 0
    for doc in documents:
        if i % 5000 == 0:
            print "正在处理第 %d/%d 行" % (i, total)
        i += 1
        words = doc.split(' ')
        for word in words:
            word_count += 1  # 统计总词数
            if word not in word_dict:
                word_dict[word] = 1
            else:
                word_dict[word] += 1

    with codecs.open(word_freq_file, "w", "utf-8") as f:
        f.write("总词语个数 %d\n------------------\n" % word_count)
        sorted_list = sorted(word_dict.items(), key=lambda item: -item[1])
        for item in sorted_list:
            # \r 就是 ^M 就是 windows 的换行符
            if item == ' ' or item[0] == '\n' or item[0] == '\t' or item[0] == '\r':
                continue
            f.write("%s\t%d\n" % (item[0], item[1]))
    t1 = datetime.datetime.now()
    print "词频统计完成，共耗时", t1 - t0


def parse_query_answer(qa_rawdata, qa_result, qa_qfile, qa_afile):
    print "处理问答对，数据源 %s" % qa_rawdata
    count = 0
    step = 0
    min_length = 12  # 最少要四个汉字，长度为 12
    qa_min_word_count = 2  # 最少词语数目，带上标点至少要 6 个
    valid_length = 7 # 每行有效的列数，如果不满足，则跳过
    qa_column = 4 # query 与 answer 所在的列（0开始）
    qa_flag = 2 # 用于判断是 query 还是 answer 的列（0 开始）
    query_flag = '0' # 表示是 query 的标志
    answer_flag = '1' # 表示是 answer 的标志
    question = ""
    answer = ""
    result = []
    question_list = []
    answer_list = []
    t0 = datetime.datetime.now()
    # 如果是其他格式的，只要做到按行读取，后面的都可以自动
    # 注意下面的 line 需要处理成数组
    # 如果分隔后列数不为 有效长度，那么说明是上一句中有换行
    # 则直接根据当前所属状态添加到对应的句子中
    # 注意字符
    f = codecs.open(qa_rawdata, "r", "gbk")
    csv_reader = csv.reader(f)
    for line in csv_reader:
        # step 0 表示初始状态，即用户没有发问，系统没有作答
        # 这时只有遇到用户问句，才进入下一阶段
        if step == 0:
            print step
            # 检测是否满足正常的格式
            if len(line) != valid_length:
                continue
            if line[qa_flag] == answer_flag: # 如果是客服回答
                continue
            question = line[qa_column]
            step = 1
        # -------------------
        # step 1 表示用户问句状态，
        elif step == 1:
            print step
            # 检测是否满足正常的格式
            if len(line) != valid_length:
                #question += line[:-1].strip()
                continue
            if line[qa_flag] == query_flag:  # 如果这一句还是用户问句，那么直接叠加到 question
                question += " " + line[qa_column]
            elif line[qa_flag] == answer_flag:
                # 如果是客服回答（并满足过滤条件，非机器人回答），则加入 answer，并进入 step 2
                answer = line[qa_column]
                step = 2
        # ---------------------
        # step 2 表示客服回答状态，
        elif step == 2:
            print step
            # 检测是否满足正常的格式
            if len(line) != valid_length:
                #answer += line[:-1].strip()
                continue
            if line[qa_flag] == answer_flag: # 如果下一句还是客服回答，那么直接叠加
                answer += " " + line[qa_column]
            elif line[qa_flag] == query_flag: # 如果下一句是用户问句，则认为一个问答对已经完成，添加到要写入的数据中，并恢复初始状态
                # 先用目前的问答对拼接成问句（需要分词）
                question = question.replace("\n", ";")
                question = question.replace("\r", "")
                answer = answer.replace("\n", ";")
                answer = answer.replace("\r", "")

                if len(question) < min_length:
                    # 如果用户问句过短，那么忽略
                    question = line[qa_column]  # -1 去掉换行符
                    step = 1  # 表示进入 step 1，用户问句阶段
                    continue

                qarr = jieba.cut(question)  # 默认是精确模式
                q_seg = " ".join(qarr)
                if len(q_seg.split(" ")) < qa_min_word_count:
                    # 如果词过少，那么忽略
                    question = line[qa_column]  # -1 去掉换行符
                    step = 1  # 表示进入 step 1，用户问句阶段
                    continue

                aarr = jieba.cut(answer)
                a_seg = " ".join(aarr)

                content = q_seg + "##" + a_seg

                # 加入到数组中，等待最后写入
                result.append(content)
                # print result
                question_list.append(q_seg)
                answer_list.append(a_seg)

                count = count + 1
                if count % 1000 == 0:
                    print "已处理 %d 个问答对" % count
                # 恢复到 step 1
                question = line[qa_column]  # -1 去掉换行符
                step = 1  # 表示进入 step 1，用户问句阶段

    # 处理最后一行的情况
    question = question.replace("\n", ";")
    question = question.replace("\r", "")
    answer = answer.replace("\n", ";")
    answer = answer.replace("\r", "")

    # 满足条件才加入
    if len(question) >= min_length:
        qarr = jieba.cut(question)  # 默认是精确模式
        q_seg = " ".join(qarr)
        if len(q_seg.split(" ")) >= qa_min_word_count:
            aarr = jieba.cut(answer)
            a_seg = " ".join(aarr)

            content = q_seg + "##" + a_seg
            # 加入到数组中，等待最后写入
            result.append(content)
            # print result
            question_list.append(q_seg)
            answer_list.append(a_seg)
            count = count + 1

    f.close()
    print "正在写入结果到 %s" % qa_result
    with codecs.open(qa_result, "w", "utf-8") as f:
        for line in result:
            try:
                f.write("%s\n" % line)
            except:
                pass
    print "正在写入问题到 %s" % qa_qfile
    with codecs.open(qa_qfile, "w", "utf-8") as fq:
        for line in question_list:
            try:
                fq.write("%s\n" % line)
            except:
                pass
    print "正在写入答案到 %s" % qa_afile
    with codecs.open(qa_afile, "w", "utf-8") as fa:
        for line in answer_list:
            try:
                fa.write("%s\n" % line)
            except:
                pass
    t1 = datetime.datetime.now()
    print "共 %d 条问答对" % count
    print "问答对完成，共耗时", t1 - t0
    return 0

def parse_knowledge_data():
    print "开始解析知识库并生成问答对"
    t0 = datetime.datetime.now()
    qcount = 0
    acount = 0

    knowledge_xlsx = xlrd.open_workbook(knowledge_data)
    sheet = knowledge_xlsx.sheet_by_index(0)
    # sheet的名称，行数，列数
    print "表名称", sheet.name
    print "共 %d 行，%d 列" % (sheet.nrows, sheet.ncols)
    result = []
    # 获取整行和整列的值（数组）
    for i in range(sheet.nrows):
        rows = sheet.row_values(i)  # 获取第四行内容
        result.append(rows)
    # print rows
    #questions = []
    # 获取标准问句
    # for q in sheet.col_values(4)[1:]:
    #    qcount += 1
    #    q = q.replace("\r", "")
    #    q = q.replace("\n", "")
    #    q = q.strip()
    #    qarr = jieba.cut(q)
    #    questions.append(" ".join(qarr))

    # 获取标准回答
    #answers = []
    # for a in sheet.col_values(5)[1:]:
    #    acount += 1
    #    a = a.replace("\r", "")
    #    a = a.replace("\n", "")
    #    a = a.replace("<br>", "")
    #    a = a.strip()
    #    aarr = jieba.cut(a)
    #    answers.append(" ".join(aarr))

    print "正在写入结果到 %s" % knowledge_result
    with codecs.open(knowledge_result, "w", "utf-8") as f:
        #    for i in range(qcount):
        for i in range(sheet.nrows):
            try:
                # f.write("%s##%s\n" % (questions[i], answers[i]))
                f.write("%s##%s\n" % (result[i][0], result[i][2]))
            except:
                pass

    #t1 = datetime.datetime.now()
    # print "共 %d 个标准问句，%d 个标准回答" % (qcount, acount)
    # print "问答对完成，共耗时", t1-t0


def split_word():
    load_raw_query()
    print "开始写入分词后的结果"
    with codecs.open(split_query, "w+", "utf-8") as r:
        for i in range(len(documents)):
            arr = jieba.cut(documents[i])
            newline = " ".join(arr)
            newline = newline[:-1] + "##\n"
            r.write(newline)
    print "为 seq2bow 数据准备完毕"


emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


def remove_emoji(text):
    return emoji_pattern.sub(r'', text)


def help():
    print "用户问句聚类测试"
    print "用法 python topic_cluster.py dict|tlda|tlsi|slda|slsi|kmeans|ap|help"
    print "dict - 生成词典并保存到 %s 中，原始分词数据在 %s 中" % (dict_path, tokenized_query)
    print "tlda - 用 LDA 模型生成 %d 个 topic，模型保存在 %s 中" % (num_topic, lda_model)
    print "tlsi - 用 LSI 模型生成 %d 个 topic，模型保存在 %s 中" % (num_topic, lsi_model)
    print "slda - 统计 LDA 聚类出来的 topic 并保存在 %s 中" % lda_result_dir
    print "slsi - 统计 LSI 聚类出来的 topic 并保存在 %s 中" % lsi_result_dir
    print "kmeans -  利用 Kmeans 聚类结果并保存在 %s 中" % kmeans_result_dir
    print "ap - 利用 AP 聚类结果并保存在 %s 中" % ap_result_dir
    print "wordfreq - 统计词频并保存在 %s 中" % word_freq_file
    print "qa - 把 %s 中的数据处理成问答对并保存在 %s 中" % (query_answer_rawdata, query_answer_result)
    print "parse - 处理 %s 知识库的问答对并保存在 %s 中" % (knowledge_data, knowledge_result)
    print "split - 分词 %s 的内容并添加 ## 符号（为 seq2bow 工具做数据准备）保存在 %s 中" % (raw_query, split_query)


if __name__ == "__main__":
    # 这个脚本是参数化的配置，更加灵活
    # ---------- 以下是参数配置 ----------
    parser = OptionParser(usage="%prog [options] arg", version="%prog 1.0")
    parser.add_option("--user_dict",
                      action="store", dest="user_dict", default="dict/default_dict.txt",
                      help="user dictionary for tokenization, default is dict/default_dict.txt")
    parser.add_option("--query_dict",
                      action="store", dest="query_dict", default="query/default.dict",
                      help="the path of dictionary that will be generated from the raw query, default is query/default.dict")
    parser.add_option("--stop_words",
                      action="store", dest="stop_words", default="dict/stop_words.txt",
                      help="the stop words for query, default is dict/stop_words.txt")
    parser.add_option("--raw_query",
                      action="store", dest="raw_query",
                      help="raw query file for the script")
    parser.add_option("--tokenized_query",
                      action="store", dest="tokenized_query", default="query/tokenized_query",
                      help="tokenized query file generated from raw query, default is query/tokenized_query")
    parser.add_option("--hidden_vector",
                      action="store", dest="hidden_vector",
                      help="hidden vector from RNN model, for clustering")
    parser.add_option("--num_topic",
                      action="store", type="int", dest="num_topic", default=500,
                      help="number of topics for clustering, default is 500")
    parser.add_option("--show_count",
                      action="store", dest="show_count", default=2500,
                      help="print information about execution every [value] records, default is 2500")
    parser.add_option("--qa_rawdata",
                      action="store", dest="qa_rawdata",
                      help="raw data file path of query-answer pair for seq2bow model")               
    parser.add_option("--qa_result",
                      action="store", dest="qa_result", default="qa/result.txt",
                      help="the filename of the parsed query-answer data for seq2bow model, default is qa/result.txt") 
    parser.add_option("--qa_qfile",
                      action="store", dest="qa_qfile", default="qa/question.txt",
                      help="the filename of the parsed query data for seq2bow model, default is qa/question.txt") 
    parser.add_option("--qa_afile",
                      action="store", dest="qa_afile", default="qa/answer.txt",
                      help="the filename of the parsed answer data for seq2bow model, default is qa/answer.txt") 

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit()

    # 载入词典
    jieba.set_dictionary(
        '/data/wdxtub/machine-learning-projects/topic_model/dict.txt.small')
    jieba.load_userdict(options.user_dict)
    time.sleep(1)

    if (args[0] == "dict"):
        CheckRet(tokenize_query(options.raw_query, options.show_count, options.user_dict, options.tokenized_query))
        CheckRet(generate_dict(options.query_dict, options.stop_words))
    elif (args[0] == "tlda"):
        CheckRet(load_tokenized_query(options.tokenized_query))
        CheckRet(generate_lda_topic(options.query_dict, options.stop_words, options.num_topic))
    elif (args[0] == "tlsi"):
        CheckRet(load_tokenized_query(options.tokenized_query))
        CheckRet(generate_lsi_topic(options.query_dict, options.stop_words, options.num_topic))
    elif (args[0] == "slda"):
        CheckRet(load_tokenized_query(options.tokenized_query))
        CheckRet(show_lda_document(options.query_dict, options.stop_words, options.num_topic, options.show_count))
    elif (args[0] == "slsi"):
        CheckRet(load_tokenized_query(options.tokenized_query))
        CheckRet(show_lsi_document(options.query_dict, options.stop_words, options.num_topic))
    elif args[0] == "kmeans" or args[0] == "ap":
        CheckRet(cluster_query(args[0], options.raw_query, options.hidden_vector, options.num_topic))
    elif (args[0] == "help"):
        help()
    elif (args[0] == "wordfreq"):
        load_tokenized_query()
        word_freq()
    elif (args[0] == "qa"):
        CheckRet(parse_query_answer(options.qa_rawdata, options.qa_result, options.qa_qfile, options.qa_afile))
    elif (args[0] == 'parse'):
        parse_knowledge_data()
    elif (args[0] == 'split'):
        split_word()
    else:
        print "未知命令"
        help()
