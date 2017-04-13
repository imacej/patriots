# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
from entity import *
import sys
sys.path.append('../code')
import cPickle as pickle

from sentiment_lstm import predict_arr

faqtable = {}
iptable = {}
records = []
knodes = []
querys = []


def load_knowledge_dict():
  # 从知识图谱中生成倒排索引，保存成词典
  # 暂时简单粗暴从已有的词典载入
  f = open("data/knowledge_dict.txt")
  for line in f:
    arr = line.split(' ')
    knodes.append(arr[0])

def load_faq_dict():
  f= open("data/beibei_faq.txt")
  for line in f:
    if (len(line) < 10): # 可能会有空行，过滤掉
      continue
    arr = line.split('\t')
    faqtable[arr[1]] = arr[0] + " " + arr[2][:-1]

def load_ip_dict():
  f= open("data/ip_file.txt")
  for line in f:
    arr = line.split('\t')
    iptable[arr[0][:-2]] = " ".join(arr[1:])
      

def filter():
  with open("data/beibei.txt") as f:
    for line in f:
      # print line,
      arr = line.split('|')
      # 过滤一波
      # 0 时间
      # 1 pid
      # 2 bid
      # 6 top1 过滤 top1:-
      # 17 source 过滤 source:test
      # 20 userip
      # -1 query 过滤 query:-
      if (arr[6].find("top1:-") != -1 or arr[17].find("source:test") != -1 or arr[-1].find("query:-") != -1):
        continue
      
      # IP 只取前 3 段
      userip = arr[20][9:-1]
      preip = ".".join(userip.split('.')[0:3])
      # 创建 Record 记录
      record = Record(arr[0][1:-2], arr[1][5:-1], arr[2][5:-1], arr[6][6:-1], preip, arr[-1][7:-2])
      # 1)查询类型，如果属于，这一步需要过滤
      doctype = faqtable.get(record.docid, "unknown")
      if (doctype != "unknown"):
        docs = doctype.split(' ')
        if (docs[1].find("售前") == -1 and docs[1].find("售中") == -1 and docs[1].find("售后") == -1):
          continue # 不在需要统计的类型中
        record.doctype = docs[1]
        record.doctext = docs[0]
      else: # 如果没有对应类型，则直接过滤
        continue
      # 2)查询地点
      location = iptable.get(record.ip, "unknown") # 如果没有找到，则为 unknown
      if (location != "unknown"):
        locs = location.split(' ')
        record.province = locs[1]
        record.city = locs[2]
      # 3)进行分词，使用精确模式，全模式会生成很多其他词语，暂时不增加复杂度
      record.words = list(jieba.cut(record.query, cut_all=False))
      # 4)提取关键词
      # 停止词语料库暂时用默认的，这里一个问句只选前五个词（也可能不足 5 个）
      # 名词 n - 人名 nr, 地名 ns, 机构团体 nt， 其他专有名词 nz
      # 动词 v - 副动词 vd， 名动词 vn
      record.keywords = jieba.analyse.extract_tags(record.query, topK=5, withWeight=False, allowPOS=('n','v','nr','ns','nt','nz','vd','vn'))
      # 5)匹配知识库节点
      for word in knodes:
        if (record.query.find(word) != -1):
          record.knodes.append(word)
      
      # 6)把句子加入到数组中，批量进行情感预测
      querys.append(record.query)
      
      # 添加到集合中
      record.displayRecord()
      records.append(record)
      #print arr[0][1:-2], arr[1][5:-1], arr[2][5:-1], arr[6][6:-1], arr[17], arr[20][9:-1], arr[-1][7:-1]
   
  # 7) 批量进行情感预测
  print "批量情感分析开始"
  probas = predict_arr(querys)
  for i, v in enumerate(probas):
    records[i].sentiment = v

  print "有效数据有", len(records)
  with open("data/records.data", 'wb') as f:
    pickle.dump(records,f, True)

  # 把数据持久化一下，保存成 json 格式
  # with open("data/records.data", 'wb') as f:
  #   for r in records:
  #     f.write(json.dumps((obj2dict(records[0]))))
  #     f.write('\n')
  print len(iptable)
  print len(knodes)
  print len(faqtable)
  print len(querys)
  print "预处理完成"


if __name__=='__main__':
  # 载入知识图谱中的词语
  jieba.load_userdict('data/knowledge_dict.txt')
  load_ip_dict() # 载入 ip 表
  load_faq_dict() # 载入 faq 表
  load_knowledge_dict() # 载入知识图谱节点表

  filter()
