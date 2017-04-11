# -*- coding: utf-8 -*-
import jieba
from entity import Record

faqtable = {}
iptable = {}
records = []

def load_faq_dict():
  with open("data/beibei_faq.txt") as f:
    for line in f:
      if (len(line) < 10): # 可能会有空行，过滤掉
        continue
      arr = line.split('\t')
      faqtable[arr[1]] = arr[0] + " " + arr[2][:-1]

def load_ip_dict():
  with open("data/ip_file.txt") as f:
    for line in f:
      arr = line.split('\t')
      iptable[arr[0]] = " ".join(arr[1:])
      

def filter():
  with open("data/bb2k.txt") as f:
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
      
      # 创建 Record 记录
      record = Record(arr[0][1:-2], arr[1][5:-1], arr[2][5:-1], arr[6][6:-1], arr[20][9:-1], arr[-1][7:-2])
      # 查询类型，如果属于，这一步需要过滤
      doctype = faqtable.get(record.docid, "unknown")
      if (doctype != "unknown"):
        docs = doctype.split(' ')
        if (docs[1].find("售前") == -1 and docs[1].find("售中") == -1 and docs[1].find("售后") == -1):
          continue # 不在需要统计的类型中
        record.doctype = docs[1]
        record.doctext = docs[0]
      # 查询地点
      location = iptable.get(record.ip, "unknown") # 如果没有找到，则为 unknown
      if (location != "unknown"):
        locs = location.split(' ')
        record.province = locs[1]
        record.city = locs[2]
      # 进行分词，使用全模式
      record.words = jieba.cut(record.query, cut_all=True)

      # 添加到集合中
      record.displayRecord()
      records.append(record)
      print arr[0][1:-2], arr[1][5:-1], arr[2][5:-1], arr[6][6:-1], arr[17], arr[20][9:-1], arr[-1][7:-1]
      
  print "有效数据有", len(records)

if __name__=='__main__':
  # 载入知识图谱中的词语，暂时还没有加入词性
  jieba.load_userdict('data/knowledge_dict.txt')
  #load_ip_dict()
  load_faq_dict()
  filter()
