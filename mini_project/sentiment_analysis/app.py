# -*- coding: utf-8 -*-
from flask import Flask, Response, json, request, render_template
from bottle import run

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd #导入Pandas
import numpy as np #导入Numpy
import jieba #导入结巴分词
import yaml
import h5py, pickle, os, datetime
from keras.models import model_from_json, save_model

from keras.utils import np_utils
from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential, model_from_yaml
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras import backend as K
from keras.layers import MaxPooling1D, Conv1D, MaxPooling1D



app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World from Data Team.'

@app.route('/sentiment', methods=['GET'])
def sentiment():
    print request.method
    if request.method == 'GET':
        query = request.args.get('query')
        sa, value = predict(unicode(query))

        #return "%s %s %s" % (sa, value, query)
        result = {}
        result['query'] = query
        result['sa'] = sa
        result['value'] = value
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json; charset=utf-8')
        resp.headers["Content-Type"] = "application/json; charset=utf-8"
        return resp

@app.route('/weibosenti', methods=['GET'])
def weibosenti():
    print request.method
    if request.method == 'GET':
        query = request.args.get('query')
        sa, value = weibo_predict(unicode(query))

        #return "%s %s %s" % (sa, value, query)
        result = {}
        result['query'] = query
        result['sa'] = sa
        result['value'] = value
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/didisenti', methods=['GET'])
def didisenti():
    print request.method
    if request.method == 'GET':
        query = request.args.get('query')
        sa, value = didi_predict(unicode(query))

        #return "%s %s %s" % (sa, value, query)
        result = {}
        result['query'] = query
        result['sa'] = sa
        result['value'] = value
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/beibeisenti', methods=['GET'])
def beibeisenti():
    print request.method
    if request.method == 'GET':
        query = request.args.get('query')
        sa, value = beibei_predict(unicode(query))

        #return "%s %s %s" % (sa, value, query)
        result = {}
        result['query'] = query
        result['sa'] = sa
        result['value'] = value
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/sentishow', methods=['GET'])
def sentishow():
    return render_template('sentishow.html')

@app.route('/wechat_senti', methods=['GET'])
def wechatsentishow():
    return render_template('wechat_sentishow.html')

@app.route('/wechat_senti_test', methods=['GET'])
def wechatsentishow_test():
    return render_template('wechat_sentishow_test.html')

# -------------------------------------------------------------------------------
# 具体计算的函数

def loaddict():
  fr = open(modeldir + '/dict.data')
  dict = pickle.load(fr)
  return dict

def loadweibodict():
  fr = open(modeldir + '/weibo/dict.data')
  wdict = pickle.load(fr)
  return wdict

def loaddididict():
  fr = open(modeldir + '/didi/dict.data')
  ddict = pickle.load(fr)
  return ddict

def loadbeibeidict():
  fr = open(modeldir + '/beibei/dict.data')
  bdict = pickle.load(fr)
  return bdict

modeldir = 'model' 

# 设置参数
# Embedding
maxlen = 128
embedding_size = 128
# Convolution
kernel_size = 5
filters = 64
pool_size = 4
# LSTM
lstm_output_size = 70
lstm_batch_size = 30
lstm_epochs = 15

print('Loading Dict Data..')
dict = loaddict()
print('Loading Weibo Dict Data..')
wdict = loadweibodict()
print('Loading Didi Dict Data..')
ddict = loaddididict()
print('Loading Beibei Dict Data..')
bdict = loadbeibeidict()

print('loading model......')
with open(modeldir + '/lstm.yml', 'r') as f:    
    yaml_string = yaml.load(f)
model = model_from_yaml(yaml_string)
print('loading weibo model......')
with open(modeldir + '/weibo/lstm.yml', 'r') as f:    
    yaml_string = yaml.load(f)
wmodel = model_from_yaml(yaml_string)
print('loading didi model......')
with open(modeldir + '/didi/lstm.yml', 'r') as f:    
    yaml_string = yaml.load(f)
dmodel = model_from_yaml(yaml_string)
print('loading beibei model......')
with open(modeldir + '/beibei/lstm.yml', 'r') as f:    
    yaml_string = yaml.load(f)
bmodel = model_from_yaml(yaml_string)


print('loading weights......')
model.load_weights(modeldir + '/lstm.h5')
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print('loading weibo weights......')
wmodel.load_weights(modeldir + '/weibo/lstm.h5')
wmodel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print('loading didi weights......')
dmodel.load_weights(modeldir + '/didi/lstm.h5')
dmodel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print('loading beibei weights......')
bmodel.load_weights(modeldir + '/beibei/lstm.h5')
bmodel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

def beibei_predict(text):
  # 把每个词转化为在词典里的数字，更新词典的计数（参考上面的格式）
  textarr = list(jieba.cut(text))
  
  textvec = []
  add = 1
  for item in textarr:
    # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
    if item in bdict['id']:
      textvec.append(bdict['id'][item])

  textvec = pd.Series(textvec)  
  textvec = sequence.pad_sequences([textvec], maxlen=maxlen)
  
  # ---- 
  

  # 需要大于 0.9
  gap = 0.9
  # 至此模型已经载入完成，可以进行预测
  #classes = model.predict_classes(textvec, verbose=1)
  proba = bmodel.predict_proba(textvec, verbose=0)
  for s in proba:
    # 找到最大概率的那个，然后输出对应结果
    index = 1
    des = u'中性情绪'
    if s[0] > s[1] and s[0] > s[2] and s[0] > 0.9:
      index = 0
      des = u'负面情绪'
    if s[1] > s[0] and s[1] > s[2]:
      index = 1
      des = u'中性情绪'
    if s[2] > s[0] and s[2] > s[1] and s[2] > 0.9:
      index = 2
      des = u'正面情绪'
    #print(des + ' ' + str(s[index]) + ' ' + text)
    return des, str(s[index])

def didi_predict(text):
  # 把每个词转化为在词典里的数字，更新词典的计数（参考上面的格式）
  textarr = list(jieba.cut(text))
  
  textvec = []
  add = 1
  for item in textarr:
    # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
    if item in ddict['id']:
      textvec.append(ddict['id'][item])

  textvec = pd.Series(textvec)  
  textvec = sequence.pad_sequences([textvec], maxlen=maxlen)

  # 至此模型已经载入完成，可以进行预测
  #classes = model.predict_classes(textvec, verbose=1)
  proba = dmodel.predict_proba(textvec, verbose=0)
  for s in proba:
    # 找到最大概率的那个，然后输出对应结果
    des = u'中性情绪'
    if s[0] > s[1]:
      index = 0
      if s[0] > 0.97:
        des = u'积极情绪'
    if s[1] > s[0]:
      index = 1
      if s[1] > 0.97:
        des = u'消极情绪'
    #print(des + ' ' + str(s[index]) + ' ' + text)
    return des, str(s[index])

def weibo_predict(text):
  # 把每个词转化为在词典里的数字，更新词典的计数（参考上面的格式）
  textarr = list(jieba.cut(text))
  
  textvec = []
  add = 1
  for item in textarr:
    # 如果不在词典里，则直接丢弃（因为出现的次数也非常少，不考虑）
    if item in wdict['id']:
      textvec.append(wdict['id'][item])

  textvec = pd.Series(textvec)  
  textvec = sequence.pad_sequences([textvec], maxlen=maxlen)

  # 至此模型已经载入完成，可以进行预测
  #classes = model.predict_classes(textvec, verbose=1)
  proba = wmodel.predict_proba(textvec, verbose=0)
  for s in proba:
    # 找到最大概率的那个，然后输出对应结果
    smax = max(s)
    if s[0] == smax:
      index = 0
      des = u'喜悦'
    if s[1] == smax:
      index = 1
      des = u'愤怒'
    if s[2] == smax:
      index = 2
      des = u'厌恶'
    if s[3] == smax:
      index = 3
      des = u'低落'
    #print(des + ' ' + str(s[index]) + ' ' + text)
    return des, str(s[index])

def predict(text):
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
  

  # 需要大于 0.9
  gap = 0.9
  # 至此模型已经载入完成，可以进行预测
  #classes = model.predict_classes(textvec, verbose=1)
  proba = model.predict_proba(textvec, verbose=0)
  for s in proba:
    # 找到最大概率的那个，然后输出对应结果
    index = 1
    des = u'中性情绪'
    if s[0] > s[1] and s[0] > s[2] and s[0] > 0.9:
      index = 0
      des = u'负面情绪'
    if s[1] > s[0] and s[1] > s[2]:
      index = 1
      des = u'中性情绪'
    if s[2] > s[0] and s[2] > s[1] and s[2] > 0.9:
      index = 2
      des = u'正面情绪'
    #print(des + ' ' + str(s[index]) + ' ' + text)
    return des, str(s[index])


# ------------------------------------------------------------------------------



if __name__ == '__main__':
    run(app=app, reloader=True, port=8776, host='0.0.0.0')
