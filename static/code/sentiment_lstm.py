# -*- coding: utf-8 -*-
from __future__ import absolute_import #导入3.x的特征函数
from __future__ import print_function

import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd #导入Pandas
import numpy as np #导入Numpy
import jieba #导入结巴分词
import h5py, pickle, os, datetime
from keras.models import model_from_json, save_model

from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential, model_from_yaml
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
sys.setrecursionlimit(1000000)

# save model http://www.linuxdiyf.com/linux/22940.html
# http://www.linuxdiyf.com/linux/22937.html
#
# http://spaces.ac.cn/archives/3414/
# https://github.com/BUPTLdy/Sentiment-Analysis
# http://blog.sina.com.cn/s/blog_735f29100102wjwu.html
# http://blog.csdn.net/weixin_36541072/article/details/53786020
# https://keras-cn.readthedocs.io/en/latest/getting_started/concepts/
# https://keras-cn.readthedocs.io/en/latest/getting_started/keras_linux/

# 设置参数
maxlen = 50
lstm_batch_size = 16
lstm_epochs = 15

datadir = ''
modeldir = '../model/lstm_didi'
testdir = ''

# 加载训练文件
def loadfile():
  print("读取语料数据")
  neg=pd.read_excel(datadir + '/neg.xls',header=None,index=None)
  mid=pd.read_excel(datadir + '/pos.xls',header=None,index=None) 
  print("读取训练语料完毕")
  print("给训练语料贴上标签")
  mid['mark']=1
  neg['mark']=0 
  print("合并语料")
  pn=pd.concat([mid,neg],ignore_index=True)
  neglen=len(neg)
  midlen=len(mid) #计算语料数目
  print('neg count:' + str(neglen))
  print('pos count:' + str(midlen))
  return pn


def tokenizer(text):
  cw = lambda x: list(jieba.cut(x)) #定义分词函数
  text['words'] = text[0].apply(cw)
  return text

def generatedict(text):
  # 计算词典并保存
  d2v_train = pd.concat([text['words']], ignore_index = True) 
  w = [] #将所有词语整合在一起
  for i in d2v_train:
    w.extend(i)
  dict = pd.DataFrame(pd.Series(w).value_counts()) #统计词的出现次数
  del w,d2v_train
  dict['id'] = list(range(1,len(dict)+1))
  # 这个 dict 需要保存下来
  outputFile = modeldir + '/dict.data'
  fw = open(outputFile, 'w')
  pickle.dump(dict,fw)
  fw.close()
  return dict

def word2index(text, dict):
  get_sent = lambda x: list(dict['id'][x])
  text['sent'] = text['words'].apply(get_sent)
  print("Pad sequences (samples x time)")
  text['sent'] = list(sequence.pad_sequences(text['sent'], maxlen=maxlen))
  return text

def getdata(text):
  x = np.array(list(text['sent']))[::2] #训练集
  y = np.array(list(text['mark']))[::2]
  xt = np.array(list(text['sent']))[1::2] #测试集
  yt = np.array(list(text['mark']))[1::2]
  xa = np.array(list(text['sent'])) #全集
  ya = np.array(list(text['mark']))
  return x,y,xt,yt,xa,ya

def train_lstm(dict,x,y,xt,yt):
  model = Sequential()
  model.add(Embedding(len(dict)+1, 256, input_length=maxlen))
  model.add(LSTM(output_dim=128, activation='sigmoid', inner_activation='hard_sigmoid'))
  model.add(Dropout(0.5))
  model.add(Dense(1))
  # model.add(Dense(input_dim = 32, output_dim = 1))
  model.add(Activation('sigmoid'))
  print ('模型构建完成')
  #model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")
  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
  print ("模型编译完成")
  model.fit(x, y, batch_size=lstm_batch_size, epochs=lstm_epochs, verbose=0)
  print ("模型训练完成")
  print ("保存模型")
  yaml_string = model.to_yaml()
  with open(modeldir + '/lstm.yml', 'w') as outfile:
    outfile.write( yaml.dump(yaml_string, default_flow_style=True) )
  model.save_weights(modeldir + '/lstm.h5')
  print ("测试集评估")
  score = model.evaluate(xt, yt, verbose=0)
  print ("准确率:",score[1])
  return model

def saveresult(model, xt, text):
  classes = model.predict_classes(xt, verbose=1) 
  proba = model.predict_proba(xt, verbose=1)

  print ("\n输出结果")
  filename = 'result.txt'
  f = open('result.txt', 'w')
  i = 1
  j = 0
  for c in classes:
    f.write(str(c))
    f.write(",")
    f.write(str(proba[j]))
    f.write(",")
    line = "".join(text['words'][i])
    f.write(line.encode('utf-8'))
    f.write("\n")
    i = i + 2
    j = j + 1
  f.close()
  print ("\n排序结果")
  num = 1
  result = []
  with open(filename, 'r') as f:
    while True:
      line = f.readline()
      if not line:
        break
      print("processing line #" + str(num))
      num = num + 1
      arr = line.split(',')
      item = (int(arr[0][1:-1]), float(arr[1][2:-1]), "".join(arr[2:]))
      result.append(item)
    result.sort(key=lambda tup:tup[1])
    print(len(result))
    f = open('sorted.txt', 'w')
    for item in result:
      f.write(str(item[0]))
      f.write(",")
      f.write(str(item[1]))
      f.write(",")
      f.write(item[2])
  print("done")

def loaddict():
  fr = open(modeldir + '/dict.data')
  dict = pickle.load(fr)
  return dict


#训练模型，并保存
def train():
  print('Loading Data...')
  pn = loadfile()
  print('Tokenising...')
  pn = tokenizer(pn)
  print('Generating Dict...')
  dict = generatedict(pn)
  print('Word to Index...')
  pn = word2index(pn, dict)
  print('Preparing data...')
  x,y,xt,yt,xa,ya = getdata(pn)
  print('Model Stage...')
  # 这里训练全量模型
  model = train_lstm(dict, xa, ya, xt, yt)
  #print('Save Test Result...')
  #saveresult(model, xt, pn)
  print("Done")
  

def batchtest(filepath):
  dict = loaddict()
  
  with open(modeldir + '/lstm.yml', 'r') as f:
    yaml_string = yaml.load(f)
  model = model_from_yaml(yaml_string)
  model.load_weights(modeldir + '/lstm.h5')
  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
  
  # 读取测试文件
  # 开始一个 for 循环，外面要统计
  test_count = 0
  correct_count = 0
  if os.path.exists(filepath):
    f = open(filepath, 'r')
    try:
      lines = f.readlines()
      for line in lines:
        if len(line) <= 0:
          continue
        else:
          arr = line.split(',')
          label = arr[0]
          test_count += 1
          text = ",".join(arr[1:])
          textarr = list(jieba.cut(text))
          textvec = []
          add = 1
          for item in textarr:
            # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
            if item in dict['id']:
              textvec.append(dict['id'][item])
          textvec = pd.Series(textvec)  
          textvec = sequence.pad_sequences([textvec], maxlen=maxlen)
          # 概率
          proba = model.predict_proba(textvec, verbose=0)
          # 判断是否计算正确
          for s in proba:
            if s[0] > 0.5 and label == '1' or s[0] <= 0.5 and label == '0':
              correct_count += 1
              print('[' + str(test_count) + ']: ' + label + ' ' + str(s[0]) + ' ' + text[:-1])
            else:
              print('[' + str(test_count) + ']:[x] ' + label + ' ' + str(s[0]) + ' ' + text[:-1])
    finally:
      f.close() # 确保关闭
  return correct_count, test_count

# 批量预测，减少内存使用，传入一个字符串数组
def predict_arr(arr):
  dict = loaddict()
  
  probas = []
  with open(modeldir + '/lstm.yml', 'r') as f:
    yaml_string = yaml.load(f)
  model = model_from_yaml(yaml_string)
  model.load_weights(modeldir + '/lstm.h5')
  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

  for s in arr:
    textarr = list(jieba.cut(s))
    textvec = []
    add = 1
    for item in textarr:
      # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
      if item in dict['id']:
        textvec.append(dict['id'][item])
    textvec = pd.Series(textvec)  
    textvec = sequence.pad_sequences([textvec], maxlen=maxlen)
    
    proba = model.predict_proba(textvec, verbose=0)
    probas.append(proba[0][0])

  return probas


def predict(text):
  print('Loading Dict Data..')
  dict = loaddict()

  # 把每个词转化为在词典里的数字，更新词典的计数（参考上面的格式）
  textarr = list(jieba.cut(text))
  
  textvec = []
  add = 1
  for item in textarr:
    # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
    if item in dict['id']:
      textvec.append(dict['id'][item])

  textvec = pd.Series(textvec)  
  textvec = sequence.pad_sequences([textvec], maxlen=maxlen)
  
  # ---- 
  print('loading model......')
  with open(modeldir + '/lstm.yml', 'r') as f:
    yaml_string = yaml.load(f)
  model = model_from_yaml(yaml_string)

  print('loading weights......')
  model.load_weights(modeldir + '/lstm.h5')
  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

  # 至此模型已经载入完成，可以进行预测
  #classes = model.predict_classes(textvec, verbose=1)
  proba = model.predict_proba(textvec, verbose=0)
  # 这里因为知识图谱暂时改变输入格式
  #for s in proba:
  #  if s[0] > 0.5:
  #    print('positive ' + str(s[0]) + ' ' + text)
  #  else:
  #    print('negative ' + str(s[0]) + ' ' + text)
  return proba[0][0]




if __name__=='__main__':
    argvs_length = len(sys.argv)
    if argvs_length >= 4:
        argvs = sys.argv
        action = argvs[1]
        if action == 'train': # 训练
            datadir = argvs[2]
            modeldir = argvs[3]
            begin = datetime.datetime.now()
            train()
            end = datetime.datetime.now()
            # 统计训练时间、模型大小，写入到 result.txt 中
            with open(modeldir + '/result.txt', "w") as f:
                f.write('训练时长: ' + str(end-begin))
        elif action == 'predict':
            modeldir = argvs[2]
            sentence = " ".join(argvs[3:])
            predict(sentence)
        elif action == 'test':
            datadir = argvs[2]
            modeldir = argvs[3]
            testdir = argvs[4]
            begin = datetime.datetime.now()
            result = batchtest(datadir+'/test.txt')
            end = datetime.datetime.now()
            # 统计训练时间、模型大小，写入到 result.txt 中
            with open(testdir + '/result.txt', "w") as f:
                f.write('测试时长: ' + str(end-begin) + '\n')
                f.write('正确率: ' + str(float(result[0])/float(result[1])) + ' (' + str(result[0]) + '/' + str(result[1]) + ')\n')
